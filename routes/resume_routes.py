from fastapi import APIRouter, HTTPException, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse, JSONResponse
from services.resume_service import generate_resume, save_resume, get_all_resumes, view_resume
from models.resume_model import Resume, Formdata
from pydantic import BaseModel
from typing import Dict, Any
from docxtpl import DocxTemplate
import urllib.parse
import io
import os

from configuration import client
from services.model import openmodel_regeneration

# Database
db = client["GenAIAmplifierDB"]
collection = db["WRICEF_Collection"]

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ─────────────────────────────────────────────
#  Static pages
# ─────────────────────────────────────────────

@router.get("/create_resume")
async def show_form(request: Request):
    return templates.TemplateResponse("business_problem_form.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


@router.get("/app", response_class=HTMLResponse)
async def read_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


# ─────────────────────────────────────────────
#  Create / save a new WRICEF item
#  FIX: use upsert so that repeated POSTs with the same
#       ricefw_number do NOT create duplicate documents.
# ─────────────────────────────────────────────

@router.post("/add")
async def add_item(form_data: Formdata):
    new_item = form_data.dict()
    new_item["fileText"] = urllib.parse.unquote(new_item["fileText"])

    # upsert=True  → insert if ricefw_number not found, skip if already exists
    # $setOnInsert → only write fields when this is a brand-new document
    result = collection.update_one(
        {"ricefw_number": new_item["ricefw_number"]},
        {"$setOnInsert": new_item},
        upsert=True,
    )

    if result.upserted_id:
        return {"message": "Item added successfully", "inserted_id": str(result.upserted_id)}
    elif result.matched_count > 0:
        # Document already existed – not an error, just a no-op
        return {"message": "Item already exists, no duplicate created"}
    else:
        return {"message": "Failed to add item"}


# ─────────────────────────────────────────────
#  Success page (reached right after /add)
#  FIX (HTTP 431): previously name + meetingNotes (full
#  file text) were passed as URL query-params, hitting
#  the 8 KB header limit.  Now only ricefwNumber and
#  wricef_type travel in the URL; everything else is
#  fetched directly from MongoDB.
# ─────────────────────────────────────────────

@router.get("/success")
async def success_page(request: Request, ricefwNumber: str, wricef_type: str):
    resume = collection.find_one({"ricefw_number": ricefwNumber})
    if not resume:
        raise HTTPException(status_code=404, detail="RICEF not found")
    return templates.TemplateResponse(
        f"{wricef_type}.html",
        {
            "request": request,
            "name": resume.get("customer", ""),
            "meetingNotes": resume.get("fileText", ""),
            "ricefwNumber": ricefwNumber,
            "resume": resume,
        },
    )


# ─────────────────────────────────────────────
#  View an existing WRICEF item
#  FIX (HTTP 431): previously name + meetingNotes (= full
#  file text, potentially thousands of chars) were passed
#  as URL query-params, blowing past the 8 KB header limit.
#  Now we just accept ricefw_number in the path and fetch
#  everything we need straight from MongoDB.
# ─────────────────────────────────────────────

@router.get("/view/{ricefw_number}", response_class=HTMLResponse)
async def view_item(request: Request, ricefw_number: str):
    resume = collection.find_one({"ricefw_number": ricefw_number})
    if not resume:
        raise HTTPException(status_code=404, detail="RICEF not found")

    wricef_type = resume.get("ricefw")
    if not wricef_type:
        raise HTTPException(status_code=400, detail="Invalid RICEF document: missing ricefw type")

    return templates.TemplateResponse(
        f"{wricef_type}.html",
        {
            "request": request,
            "name": resume.get("customer", ""),
            "meetingNotes": resume.get("fileText", ""),
            "ricefw_number": ricefw_number,
            "resume": resume,
        },
    )


# ─────────────────────────────────────────────
#  Lightweight data API used by WRICEF templates
#  to fetch customer name and fileText without
#  putting large content in the URL (HTTP 431 fix).
# ─────────────────────────────────────────────

@router.get("/api/wricef_data/{ricefw_number}")
async def get_wricef_data(ricefw_number: str):
    doc = collection.find_one(
        {"ricefw_number": ricefw_number},
        {"_id": 0, "customer": 1, "fileText": 1},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="RICEF not found")
    return {"customer": doc.get("customer", ""), "fileText": doc.get("fileText", "")}


# ─────────────────────────────────────────────
#  List all WRICEFs
# ─────────────────────────────────────────────

@router.get("/listofwricefs")
async def get_ricefs_list(request: Request):
    # Only fetch the fields we actually display in the table.
    # fileText is intentionally excluded from this query –
    # we no longer put it in the URL so there is no need to
    # load it here at all.
    ricefs_list = list(
        collection.find({}, {"_id": 0, "ricefw_number": 1, "customer": 1})
    )
    return templates.TemplateResponse(
        "listofwricefs.html", {"request": request, "ricefs_list": ricefs_list}
    )


# ─────────────────────────────────────────────
#  Generate AI response for a WRICEF item
# ─────────────────────────────────────────────

@router.post("/generate_response")
async def create_resume(
    client_problem: str = Form(...),
    client_name: str = Form(...),
    ricefwNumber: str = Form(...),
):
    print(f"Received client_problem: {client_problem}")
    print(f"Received client_name: {client_name}")
    print(f"Received ricefwNumber: {ricefwNumber}")

    resume = collection.find_one({"ricefw_number": ricefwNumber})
    if not resume:
        raise HTTPException(status_code=404, detail="RICEF not found")

    wricef_type = resume["ricefw"]
    print(f"Received wricefType: {wricef_type}")

    generated_resume = generate_resume(client_problem, wricef_type)
    print(f"Generated resume: {generated_resume}")

    new_field_data = {
        "generated_resume": generated_resume,
        "client_problem": client_problem,
    }

    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$push": new_field_data},
    )

    if result.matched_count > 0:
        print("Document updated successfully!")
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Client not found in the database")


# ─────────────────────────────────────────────
#  Section 2 (POST – receives JSON body)
# ─────────────────────────────────────────────

@router.post("/section2", response_class=HTMLResponse)
async def open_section(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)
        resumes = get_all_resumes()
        return templates.TemplateResponse(
            "section2.html", {"request": request, "data": data, "resumes": resumes}
        )
    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": "Failed to process data."}, status_code=500)


# ─────────────────────────────────────────────
#  Resume view (file-based, legacy)
# ─────────────────────────────────────────────

@router.get("/resume_view/{resume_name}")
async def view(resume_name: str, request: Request):
    print(resume_name)
    resume = view_resume(resume_name)
    print(resume)
    if isinstance(resume, list):
        return templates.TemplateResponse(
            "riceffile.html", {"request": request, "resume": resume}
        )
    else:
        raise HTTPException(status_code=404, detail="RICEF not found")


# ─────────────────────────────────────────────
#  Download WRICEF as .docx
# ─────────────────────────────────────────────

def get_document_by_customer(ricefw_number: str):
    return collection.find_one({"ricefw_number": ricefw_number})


@router.get("/resume_download/{ricefw_number}")
async def download_pdf(ricefw_number: str):
    document = get_document_by_customer(ricefw_number)

    if not document:
        raise HTTPException(status_code=404, detail="RICEF not found")

    if "ricefw" not in document or not document["ricefw"]:
        raise HTTPException(status_code=400, detail="Invalid RICEF document data")

    template_path = f"templates/{document['ricefw']}.docx"

    try:
        template = DocxTemplate(template_path)
        template.render({"resume": document})

        byte_io = io.BytesIO()
        template.save(byte_io)
        byte_io.seek(0)

        return Response(
            byte_io.read(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename=RICEF_{ricefw_number}.docx"},
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404, detail=f"Template file '{template_path}' not found"
        )


# ─────────────────────────────────────────────
#  Update customer data (section-level edit)
# ─────────────────────────────────────────────

class UpdateData(BaseModel):
    section: str
    data: Dict[str, Any]


@router.post("/update_customer_data")
async def update_customer_data(request: Request, update_data: UpdateData):
    print("Received UpdateData object:", update_data)
    print("Section:", update_data.section)
    print("Data:", update_data.data)

    customer_name = request.query_params.get("customerName")
    if not customer_name:
        raise HTTPException(status_code=400, detail="customerName query parameter is required")

    document = collection.find_one({"customer": customer_name})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    update_data_array = [{"k": k, "v": v} for k, v in update_data.data.items()]

    pipeline = [
        {
            "$set": {
                "generated_resume": {
                    "$map": {
                        "input": "$generated_resume",
                        "as": "item",
                        "in": {
                            "$mergeObjects": [
                                "$$item",
                                {
                                    "$arrayToObject": {
                                        "$filter": {
                                            "input": update_data_array,
                                            "as": "upd",
                                            "cond": {
                                                "$in": [
                                                    "$$upd.k",
                                                    {
                                                        "$map": {
                                                            "input": {"$objectToArray": "$$item"},
                                                            "as": "field",
                                                            "in": "$$field.k",
                                                        }
                                                    },
                                                ]
                                            },
                                        }
                                    }
                                },
                            ]
                        },
                    }
                }
            }
        }
    ]

    result = collection.update_one({"_id": document["_id"]}, pipeline)
    return {"success": True, "modified_count": result.modified_count}


# ─────────────────────────────────────────────
#  Regeneration endpoint
# ─────────────────────────────────────────────

@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...),
):
    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    document = collection.find_one({"ricefw_number": ricefwNumber})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    generated_resume = document.get("generated_resume", [])
    if index_value < 0 or index_value >= len(generated_resume):
        raise HTTPException(status_code=400, detail="section_index out of range.")

    current_response = generated_resume[index_value].get("response", "")
    previous_response = (
        generated_resume[index_value - 1].get("response", "") if index_value > 0 else ""
    )

    wricef_type = document.get("ricefw", "")
    print(f"Received wricefType: {wricef_type}")

    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        wricefType=wricef_type,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value,
    )

    generated_resume[index_value] = new_enhanced_response

    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}