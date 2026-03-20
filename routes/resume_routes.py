from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, FileResponse
from services.resume_service import generate_resume, save_resume, get_all_resumes, view_resume
from models.resume_model import Resume, Formdata
import urllib.parse


import os
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from configuration import client
from typing import Dict
from services.model import openmodel_regeneration

#Data Base 
db = client["GenAIAmplifierDB"]
collection = db["WRICEF_Collection"]



router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/create_resume")
async def show_form(request: Request):
    return templates.TemplateResponse("business_problem_form.html", {"request": request})


"""
@router.post("/generate_response")
async def create_resume(client_problem: str = Form(...), client_name: str = Form(...)):
    # Log input values
    print(f"Received client_problem: {client_problem}")
    print(f"Received client_name: {client_name}")

    # Generate the resume
    generated_resume = generate_resume(client_problem, client_name)
    print(f"Generated resume: {generated_resume}")

    # Create a Resume instance (include client_name if the model requires it)
    resume = Resume(client_problem=client_problem, generated_resume=generated_resume, client_name=client_name)

    # Save to the database
    resume_dict = resume.dict()
    resume_id = save_resume(resume_dict)

    if resume_id:
        print(f"Resume saved with ID: {resume_id}")
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=500, detail="Failed to save resume")"""

"""
@router.get("/")
async def list_resumes(request: Request):
    resumes = get_all_resumes()
    return templates.TemplateResponse("resume_list.html", {"request": request, "resumes": resumes})"""

@router.get("/", response_class=HTMLResponse)
async def get_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


@router.get("/app", response_class=HTMLResponse)
async def read_app(request: Request):
    return templates.TemplateResponse("app.html", {"request": request})


"""
@router.get("/section1.html", response_class=HTMLResponse)
async def open_section1(request: Request):
    # Extract query parameters from the request URL
    query_params = request.query_params

    # You can access each parameter like this:
    ricefw = query_params.get("ricefw")
    customer = query_params.get("customer")
    ricefw_number = query_params.get("ricefw-number")
    module = query_params.get("module")
    specification = query_params.get("specification")
    description = query_params.get("description")
    related_ricefw = query_params.get("related-ricefw")
    created_by = query_params.get("created-by")
    document_date = query_params.get("document-date")
    completion_date = query_params.get("completion-date")
    client_owner_name = query_params.get("client-owner-name")
    client_owner_company = query_params.get("client-owner-company")
    client_owner_email = query_params.get("client-owner-email")
    client_owner_phone = query_params.get("client-owner-phone")
    functional_owner_name = query_params.get("functional-owner-name")
    functional_owner_company = query_params.get("functional-owner-company")
    functional_owner_email = query_params.get("functional-owner-email")
    functional_owner_phone = query_params.get("functional-owner-phone")
    technical_owner_name = query_params.get("technical-owner-name")
    technical_owner_company = query_params.get("technical-owner-company")
    technical_owner_email = query_params.get("technical-owner-email")
    technical_owner_phone = query_params.get("technical-owner-phone")
    developer_name = query_params.get("developer-name")
    developer_company = query_params.get("developer-company")
    developer_email = query_params.get("developer-email")
    developer_phone = query_params.get("developer-phone")
    fileText = query_params.get("fileText")
    
    # Prepare data to pass to the template
    params_data = {
        "ricefw": ricefw,
        "customer": customer,
        "ricefw_number": ricefw_number,
        "module": module,
        "specification": specification,
        "description": description,
        "related_ricefw": related_ricefw,
        "created_by": created_by,
        "document_date": document_date,
        "completion_date": completion_date,
        "client_owner_name": client_owner_name,
        "client_owner_company": client_owner_company,
        "client_owner_email": client_owner_email,
        "client_owner_phone": client_owner_phone,
        "functional_owner_name": functional_owner_name,
        "functional_owner_company": functional_owner_company,
        "functional_owner_email": functional_owner_email,
        "functional_owner_phone": functional_owner_phone,
        "technical_owner_name": technical_owner_name,
        "technical_owner_company": technical_owner_company,
        "technical_owner_email": technical_owner_email,
        "technical_owner_phone": technical_owner_phone,
        "developer_name": developer_name,
        "developer_company": developer_company,
        "developer_email": developer_email,
        "developer_phone": developer_phone,
        "fileText": fileText
    }
    print("*" * 100)
    print("\n")
    print(params_data['customer'])

    resumes = get_all_resumes()

    # Return the template with the data
    return templates.TemplateResponse("section1.html", {"request": request, "params_data": params_data, "resumes":resumes})

"""

@router.post("/section2", response_class=HTMLResponse)  # Changed to POST
async def open_section(request: Request):

    try:
        data = await request.json()  # Expecting a JSON body for POST request
        print("Received data:", data)

        resumes = get_all_resumes()  # Assuming this function retrieves all resumes

        # Return the template with the data
        return templates.TemplateResponse("section2.html", {"request": request, "data": data, "resumes": resumes})

    except Exception as e:
        print("Error:", e)
        return JSONResponse(content={"error": "Failed to process data."}, status_code=500)



@router.get("/resume_view/{resume_name}")
async def view(resume_name: str, request: Request):
    # Call the synchronous function to retrieve the resume data
    print(resume_name)
    resume = view_resume(resume_name)
    print(resume)
    if isinstance(resume, list):
        print("if block of view excuting")
        return templates.TemplateResponse("riceffile.html", {"request": request, "resume": resume})
    else:
        raise HTTPException(status_code=404, detail="RICEF not found")



# new code 
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import FileResponse
from docxtpl import DocxTemplate
import io


"""
@router.get("/resume_download/{resume_name}")
async def download_pdf(resume_name: str, request: Request):
    # Retrieve the resume data
    resume = view_resume(resume_name)
    if isinstance(resume, list):
        # Load Word template and populate with data
        template = DocxTemplate("templates/template.docx")
        template.render({"resume": resume})

        # Save to a BytesIO stream instead of file
        byte_io = io.BytesIO()
        template.save(byte_io)
        byte_io.seek(0)

        # Return the Word document as a downloadable file
        return Response(byte_io.read(), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={
            "Content-Disposition": f"attachment; filename=RICEF_{resume_name}.docx"
        })
    else:
        raise HTTPException(status_code=404, detail="Resume not found")


"""


#working now 

"""
@router.post("/add")
async def add_item(
    ricefw: str = Form(...),
    customer: str = Form(...),
    ricefw_number: str = Form(...),
    module: str = Form(...),
    specification: str = Form(...),
    description: str = Form(...),
    related_ricefw: str = Form(...),
    created_by: str = Form(...),
    document_date: str = Form(...),
    completion_date: str = Form(...),
    client_owner_name: str = Form(...),
    client_owner_company: str = Form(...),
    client_owner_email: str = Form(...),
    client_owner_phone: str = Form(...),
    functional_owner_name: str = Form(...),
    functional_owner_company: str = Form(...),
    functional_owner_email: str = Form(...),
    functional_owner_phone: str = Form(...),
    technical_owner_name: str = Form(...),
    technical_owner_company: str = Form(...),
    technical_owner_email: str = Form(...),
    technical_owner_phone: str = Form(...),
    developer_name: str = Form(...),
    developer_company: str = Form(...),
    developer_email: str = Form(...),
    developer_phone: str = Form(...),
):
    # Create a dictionary from the form data
    new_item = Formdata(
        ricefw=ricefw,
        customer=customer,
        ricefw_number=ricefw_number,
        module=module,
        specification=specification,
        description=description,
        related_ricefw=related_ricefw,
        created_by=created_by,
        document_date=document_date,
        completion_date=completion_date,
        client_owner_name=client_owner_name,
        client_owner_company=client_owner_company,
        client_owner_email=client_owner_email,
        client_owner_phone=client_owner_phone,
        functional_owner_name=functional_owner_name,
        functional_owner_company=functional_owner_company,
        functional_owner_email=functional_owner_email,
        functional_owner_phone=functional_owner_phone,
        technical_owner_name=technical_owner_name,
        technical_owner_company=technical_owner_company,
        technical_owner_email=technical_owner_email,
        technical_owner_phone=technical_owner_phone,
        developer_name=developer_name,
        developer_company=developer_company,
        developer_email=developer_email,
        developer_phone=developer_phone,
    )

    # Insert the data into the database (assuming collection is your database collection)
    await collection.insert_one(new_item.dict())  # Convert to dictionary for DB insertion

    return JSONResponse(content={"message": "Item added successfully"})"""



@router.post("/add")
async def add_item(form_data: Formdata):
    # Convert Pydantic model to dictionary
    new_item = form_data.dict()
    fileText = new_item['fileText']
    fileText = urllib.parse.unquote(fileText)
    new_item['fileText'] = fileText

    # Insert into your MongoDB collection
    result = collection.insert_one(new_item)

    # Check if the insertion was successful
    if result.inserted_id:
        return {"message": "Item added successfully", "inserted_id": str(result.inserted_id)}
    else:
        return {"message": "Failed to add item"}





@router.get("/success")
async def success_page(request: Request, name: str, meetingNotes: str, ricefwNumber: str, wricef_type: str):
    resume = collection.find_one({"ricefw_number":ricefwNumber})

    return templates.TemplateResponse(f"{wricef_type}.html", {"request": request, "name": name, "meetingNotes": meetingNotes, "ricefwNumber": ricefwNumber, "resume":resume})



@router.get("/view/{ricefw_number}", response_class=HTMLResponse)
async def view_item(request: Request, ricefw_number: str, name: str, meetingNotes: str):
    resume = collection.find_one({"ricefw_number": ricefw_number})
    wricefType = resume["ricefw"]
    return templates.TemplateResponse(f"{wricefType}.html", {
        "request": request,
        "name": name,
        "meetingNotes": meetingNotes,
        "ricefw_number": ricefw_number,
        "resume": resume
    })


@router.post("/generate_response")
async def create_resume(client_problem: str = Form(...), client_name: str = Form(...), ricefwNumber: str = Form(...)):
    # Log input values
    print(f"Received client_problem: {client_problem}")
    print(f"Received client_name: {client_name}")
    print(f"Received ricefwNumber: {ricefwNumber}")

    resume = collection.find_one({"ricefw_number": ricefwNumber})
    wricefType = resume["ricefw"]

    print(f"Received wricefType: {wricefType}")

    # Generate the resume
    generated_resume = generate_resume(client_problem, wricefType)
    print(f"Generated resume: {generated_resume}")

    # New dictionary to be added
    new_field_data = {
        "generated_resume": generated_resume,
        "client_problem": client_problem
    }

    # Search for an existing document with the matching client_name
    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        # {"customer": client_name},  # Match condition
        {"$push": new_field_data}  # Add new field or update existing
    )

    if result.matched_count > 0:
        print("Document updated successfully!")
        return RedirectResponse(url="/", status_code=303)
    else:
        raise HTTPException(status_code=404, detail="Client not found in the database")
    




# Function to get document by ricefw number
def get_document_by_customer(ricefw_number: str):
    document = collection.find_one({"ricefw_number": ricefw_number})
    return document


# Route to download the resume
@router.get("/resume_download/{ricefw_number}")
async def download_pdf(ricefw_number: str):
    # Retrieve the document data from the database
    document = get_document_by_customer(ricefw_number)
    
    if not document:
        raise HTTPException(status_code=404, detail="RICEF not found")

    # Ensure "ricefw" key exists in document
    if "ricefw" not in document or not document["ricefw"]:
        raise HTTPException(status_code=400, detail="Invalid RICEF document data")

    template_path = f"templates/{document['ricefw']}.docx"

    try:
        # Load Word template and populate it with the document data
        template = DocxTemplate(template_path)
        template.render({"resume": document})

        # Save to a BytesIO stream instead of file
        byte_io = io.BytesIO()
        template.save(byte_io)
        byte_io.seek(0)

        # Return the Word document as a downloadable file
        return Response(byte_io.read(), media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={
            "Content-Disposition": f"attachment; filename=RICEF_{ricefw_number}.docx"
        })
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Template file '{template_path}' not found")







from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Dict, Any





# Pydantic model for the data to be updated
class UpdateData(BaseModel):
    section: str
    data: Dict[str, Any]

"""
@router.post("/update_customer_data")
async def update_customer_data(request: Request, update_data: UpdateData):
    # Extract 'customerName' parameter from the query string
    customer_name = request.query_params.get('customerName')
    if not customer_name:
        raise HTTPException(status_code=400, detail="customerName query parameter is required")

    # Find the document by customer name
    document =  collection.find_one({"customer": customer_name})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    print("document")
    print(document)

    print("/n")
    print("Update data")
    print(update_data)

    # Update the specified section in the document
    if update_data.section in document:
         collection.update_one(
            {"_id": document["_id"]},
            {"$set": {update_data.section: update_data.data}}
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid section name")

    return {"success": True}
"""







@router.post("/update_customer_data")
async def update_customer_data(request: Request, update_data: UpdateData):
    # Print the entire UpdateData object
    print("Received UpdateData object:", update_data)

    # Extract and print the 'section' and 'data' attributes
    print("Section:", update_data.section)
    print("Data:", update_data.data)

    # Extract the customerName query parameter
    customer_name = request.query_params.get("customerName")
    if not customer_name:
        raise HTTPException(status_code=400, detail="customerName query parameter is required")

    # Find the document by customer name
    document = collection.find_one({"customer": customer_name})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # Convert the update_data.data dictionary into an array of key-value pairs
    update_data_array = [{"k": k, "v": v} for k, v in update_data.data.items()]

    # Build the update pipeline
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
                                                    {"$map": {"input": {"$objectToArray": "$$item"}, "as": "field", "in": "$$field.k"}}
                                                ]
                                            }
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    ]

    # Execute the update pipeline
    result = collection.update_one({"_id": document["_id"]}, pipeline)

    return {"success": True, "modified_count": result.modified_count}



"""
@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...)
):
    # Convert section_index to integer.
    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    # Find the document by ricefw_number (note: field name in document is ricefw_number).
    document = collection.find_one({"ricefw_number": ricefwNumber})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    generated_resume = document.get("generated_resume", [])
    if index_value < 0 or index_value >= len(generated_resume):
        raise HTTPException(status_code=400, detail="section_index out of range.")

    # Retrieve the current response from the target section.
    # (Using .get() to safely extract "response" if present; otherwise default to empty string.)
    current_response = generated_resume[index_value].get("response", "")
    # Retrieve the previous response from the previous section (if available).
    previous_response = generated_resume[index_value - 1].get("response", "") if index_value > 0 else ""

    # Generate the new enhanced response.
    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        client_name=client_name,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value
    )

    # Update only the targeted dictionary within the generated_resume list.
    # For example, add/update a key "regenerated_response" with the new enhanced response.
    generated_resume[index_value].update({"regenerated_response": new_enhanced_response})

    # Update the document in the database.
    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}"""


"""
@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...)
):
    # Convert section_index to integer.
    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    # Find the document by ricefw_number.
    document = collection.find_one({"ricefw_number": ricefwNumber})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    generated_resume = document.get("generated_resume", [])
    if index_value < 0 or index_value >= len(generated_resume):
        raise HTTPException(status_code=400, detail="section_index out of range.")

    # Retrieve the current response from the target section.
    current_response = generated_resume[index_value].get("response", "")
    # Retrieve the previous response from the previous section (if available).
    previous_response = generated_resume[index_value - 1].get("response", "") if index_value > 0 else ""

    # Generate the new enhanced response.
    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        client_name=client_name,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value
    )

    # Replace the current response with the new enhanced response.
    generated_resume[index_value]["response"] = new_enhanced_response

    # Update the document in the database.
    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}"""


"""

@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...)
):
    # Convert section_index to integer.
    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    # Find the document by ricefw_number.
    document = collection.find_one({"ricefw_number": ricefwNumber})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    generated_resume = document.get("generated_resume", [])
    if index_value < 0 or index_value >= len(generated_resume):
        raise HTTPException(status_code=400, detail="section_index out of range.")

    # Retrieve the current response from the target section.
    current_response = generated_resume[index_value].get("response", "")
    # Retrieve the previous response from the previous section (if available).
    previous_response = generated_resume[index_value - 1].get("response", "") if index_value > 0 else ""

    # Generate the new enhanced response.
    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        client_name=client_name,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value
    )

    # Replace the entire dictionary at the index with a new dictionary using the index_value as key.
    generated_resume[index_value] = { str(index_value): new_enhanced_response }

    # Update the document in the database.
    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}"""



@router.post("/regeneration")
async def regeneration(
    client_name: str = Form(...),
    meetingNotes: str = Form(...),
    section_index: str = Form(...),
    ricefwNumber: str = Form(...)
):
    # Convert section_index to integer.
    try:
        index_value = int(section_index)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid section_index. Must be an integer.")

    # Find the document by ricefw_number.
    document = collection.find_one({"ricefw_number": ricefwNumber})
    if not document:
        raise HTTPException(status_code=404, detail="Document not found.")

    generated_resume = document.get("generated_resume", [])
    if index_value < 0 or index_value >= len(generated_resume):
        raise HTTPException(status_code=400, detail="section_index out of range.")

    # Retrieve the current response from the target section.
    current_response = generated_resume[index_value].get("response", "")
    # Retrieve the previous response from the previous section (if available).
    previous_response = generated_resume[index_value - 1].get("response", "") if index_value > 0 else ""


    resume = collection.find_one({"ricefw_number": ricefwNumber})
    wricefType = resume["ricefw"]

    print(f"Received wricefType: {wricefType}")

    # Generate the new enhanced response.
    new_enhanced_response = openmodel_regeneration(
        client_business_requirement=meetingNotes,
        wricefType=wricefType,
        previous_response=previous_response,
        current_response=current_response,
        index_value=index_value
    )

    # Replace the current response with the new enhanced response.
    generated_resume[index_value] = new_enhanced_response

    # Update the document in the database.
    result = collection.update_one(
        {"ricefw_number": ricefwNumber},
        {"$set": {"generated_resume": generated_resume}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update document.")

    return {"success": True, "new_response": new_enhanced_response}








@router.get("/listofwricefs")
async def get_ricefs_list(request: Request):
    ricefs_list = list(collection.find({}, {"_id": 0, "ricefw_number": 1, "customer": 1, "fileText":1}))  # Fetch ricefs_number & customer_name
    return templates.TemplateResponse("listofwricefs.html", {"request": request, "ricefs_list": ricefs_list})