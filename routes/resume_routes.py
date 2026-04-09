import re
import logging
import urllib.parse
import io
import zipfile
import xml.etree.ElementTree as ET

from fastapi import APIRouter, HTTPException, Request, Form, Response, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any
from docxtpl import DocxTemplate

from configuration import client
from models.resume_model import Resume, Formdata
from services.resume_service import generate_resume, save_resume, get_all_resumes, view_resume
from services.model import openmodel_regeneration
from services.llm_client import ALLOWED_WRICEF_TYPES

logger = logging.getLogger(__name__)

db = client["GenAIAmplifierDB"]
collection = db["WRICEF_Collection"]

router = APIRouter()
templates = Jinja2Templates(directory="templates")

RICEFW_NUMBER_PATTERN = re.compile(r'^.+$')
MAX_GENERATED_RESUME_ENTRIES = 20


def _validate_ricefw_number(ricefw_number: str) -> str:
    if not RICEFW_NUMBER_PATTERN.match(ricefw_number):
        raise HTTPException(status_code=400, detail="Invalid ricefw_number format")
    return ricefw_number


def _validate_wricef_type(wricef_type: str) -> str:
    if wricef_type not in ALLOWED_WRICEF_TYPES:
        raise HTTPException(status_code=400, detail=f"Invalid wricef type '{wricef_type}'")
    return wricef_type


@router.get("/create_resume")
async def show_form(request: Request):
    return templates.TemplateResponse("business_problem_form.html", {"request": request})


@router.get("/", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


@router.get("/app", response_class=HTMLResponse)
async def read_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


@router.post("/parse_file")
async def parse_file(file: UploadFile = File(...)):
    filename = file.filename or ""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    allowed = {"txt", "vtt", "docx"}
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type '.{ext}'. Allowed: {', '.join(sorted(allowed))}")

    content = await file.read()

    if ext in ("txt", "vtt"):
        text = content.decode("utf-8", errors="replace")
        if ext == "vtt":
            lines = []
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("WEBVTT") or line.startswith("NOTE"):
                    continue
                if "-->" in line:
                    continue
                if re.match(r"^\d+$", line):
                    continue
                lines.append(line)
            text = " ".join(lines)
    elif ext == "docx":
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            with z.open("word/document.xml") as f:
                tree = ET.parse(f)
        paragraphs = []
        for para in tree.findall(".//w:p", ns):
            parts = [node.text or "" for node in para.findall(".//w:t", ns)]
            line = "".join(parts).strip()
            if line:
                paragraphs.append(line)
        text = "\n".join(paragraphs)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    return {"text": text}


@router.post("/add")
async def add_item(form_data: Formdata):
    new_item = form_data.model_dump()
    new_item["fileText"] = urllib.parse.unquote(new_item["fileText"])

    result = await collection.update_one(
        {"ricefw_number": new_item["ricefw_number"]},
        {"$setOnInsert": new_item},
        upsert=True,
    )

    if result.upserted_id:
        return {"message": "Item added successfully", "inserted_id": str(result.upserted_id)}
    elif result.matched_count > 0:
        return {"message": "Item already exists, no duplicate created"}
    else:
        return {"message": "Failed to add item"}


@router.get("/success")
async def success_page(request: Request, ricefwNumber: str, wricef_type: str):
    ricefwNumber = urllib.parse.unquote(ricefwNumber)
    ricefwNumber = _validate_ricefw_number(ricefwNumber)
    _validate_wricef_type(wricef_type)
    resume = await collection.find_one({"ricefw_number": ricefwNumber})
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


@router.get("/view/{ricefw_number:path}", response_class=HTMLResponse)
async def view_item(request: Request, ricefw_number: str):
    ricefw_number = urllib.parse.unquote(ricefw_number)
    ricefw_number = _validate_ricefw_number(ricefw_number)
    resume = await collection.find_one({"ricefw_number": ricefw_number})
    if not resume:
        raise HTTPException(status_code=404, detail="RICEF not found")

    wricef_type = resume.get("ricefw")
    if not wricef_type:
        raise HTTPException(status_code=400, detail="Invalid RICEF document: missing ricefw type")
    _validate_wricef_type(wricef_type)

    return templates.TemplateResponse(
        f"{wricef_type}.html",
        {
            "request": request,
            "name": resume.get("customer", ""),
            "meetingNotes": resume.get("fileText", ""),
            "ricefw_number": ricefw_number,
            "ricefwNumber": ricefw_number,
            "resume": resume,
        },
    )


@router.get("/api/wricef_data/{ricefw_number:path}")
async def get_wricef_data(ricefw_number: str):
    ricefw_number = urllib.parse.unquote(ricefw_number)
    ricefw_number = _validate_ricefw_number(ricefw_number)
    doc = await collection.find_one(
        {"ricefw_number": ricefw_number},
        {"_id": 0, "customer": 1, "fileText": 1, "specification": 1},
    )
    if not doc:
        raise HTTPException(status_code=404, detail="RICEF not found")
    return {"customer": doc.get("customer", ""), "fileText": doc.get("fileText", ""), "specification": doc.get("specification", "")}


@router.get("/listofwricefs")
async def get_ricefs_list(request: Request):
    ricefs_list = [
        doc async for doc in collection.find({}, {"_id": 0, "ricefw_number": 1, "customer": 1})
    ]
    return templates.TemplateResponse(
        "listofwricefs.html", {"request": request, "ricefs_list": ricefs_list}
    )


@router.post("/generate_response")
async def create_resume(
    client_problem: str = Form(...),
    client_name: str = Form(...),
    ricefwNumber: str = Form(...),
):
    ricefwNumber = _validate_ricefw_number(ricefwNumber)
    resume = await collection.find_one({"ricefw_number": ricefwNumber})
    if not resume:
        raise HTTPException(status_code=404, detail="RICEF not found")

    wricef_type = resume["ricefw"]
    _validate_wricef_type(wricef_type)

    file_text = urllib.parse.unquote(resume.get("fileText", ""))
    prefix = client_problem.split(" ")[0] if client_problem else ""
    actual_problem = f"{prefix} {file_text}".strip()

    logger.info("Generating response for ricefwNumber=%s wricefType=%s", ricefwNumber, wricef_type)
    generated_resume = generate_resume(actual_problem, wricef_type)

    result = await collection.update_one(
        {"ricefw_number": ricefwNumber},
        {
            "$push": {
                "generated_resume": {
                    "$each": [generated_resume],
                    "$slice": -MAX_GENERATED_RESUME_ENTRIES,
                },
                "client_problem": {
                    "$each": [actual_problem],
                    "$slice": -MAX_GENERATED_RESUME_ENTRIES,
                },
            }
        },
    )

    if result.matched_count > 0:
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Client not found in the database")


@router.post("/section2", response_class=HTMLResponse)
async def open_section(request: Request):
    try:
        data = await request.json()
        resumes = await get_all_resumes()
        return templates.TemplateResponse(
            "section2.html", {"request": request, "data": data, "resumes": resumes}
        )
    except Exception as e:
        logger.error("Error in /section2: %s", e)
        return JSONResponse(content={"error": "Failed to process data."}, status_code=500)


@router.get("/resume_view/{resume_name}")
async def view(resume_name: str, request: Request):
    resume = await view_resume(resume_name)
    if isinstance(resume, list):
        return templates.TemplateResponse(
            "riceffile.html", {"request": request, "resume": resume}
        )
    else:
        raise HTTPException(status_code=404, detail="RICEF not found")


async def get_document_by_customer(ricefw_number: str):
    _validate_ricefw_number(ricefw_number)
    return await collection.find_one({"ricefw_number": ricefw_number})


@router.get("/resume_download/{ricefw_number:path}")
async def download_pdf(ricefw_number: str):
    ricefw_number = urllib.parse.unquote(ricefw_number)
    document = await get_document_by_customer(ricefw_number)
    if not document:
        raise HTTPException(status_code=404, detail="RICEF not found")

    wricef_type_val = document.get("ricefw", "")
    _validate_wricef_type(wricef_type_val)

    template_path = f"templates/{wricef_type_val}.docx"
    try:
        template = DocxTemplate(template_path)
        template.render({"resume": document})

        byte_io = io.BytesIO()
        template.save(byte_io)
        byte_io.seek(0)

        return Response(
            byte_io.read(),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={document.get('specification', ricefw_number) or ricefw_number}.docx"},
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template file '{template_path}' not found")


class UpdateData(BaseModel):
    section: str
    data: Dict[str, Any]


@router.post("/update_customer_data")
async def update_customer_data(request: Request, update_data: UpdateData):
    customer_name = request.query_params.get("customerName")
    if not customer_name:
        raise HTTPException(status_code=400, detail="customerName query parameter is required")

    document = await collection.find_one({"customer": customer_name})
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

    result = await collection.update_one({"_id": document["_id"]}, pipeline)
    return {"success": True, "modified_count": result.modified_count}


@router.delete("/delete/{ricefw_number:path}")
async def delete_wricef(ricefw_number: str):
    ricefw_number = urllib.parse.unquote(ricefw_number)
    ricefw_number = _validate_ricefw_number(ricefw_number)
    result = await collection.delete_one({"ricefw_number": ricefw_number})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="RICEF not found")
    return {"success": True}


@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...),
):
    ricefwNumber = _validate_ricefw_number(ricefwNumber)

    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    document = await collection.find_one({"ricefw_number": ricefwNumber})
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
    _validate_wricef_type(wricef_type)

    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        wricefType=wricef_type,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value,
    )

    generated_resume[index_value] = new_enhanced_response

    result = await collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}
