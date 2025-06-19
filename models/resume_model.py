from pydantic import BaseModel

class Resume(BaseModel):
    client_problem: str
    generated_resume: dict
    client_name: str


class Formdata(BaseModel):
    ricefw: str
    customer: str
    ricefw_number: str
    module: str
    specification: str
    description: str
    related_ricefw: str
    created_by: str
    document_date: str
    completion_date: str
    client_owner_name: str
    client_owner_company: str
    client_owner_email: str
    client_owner_phone: str
    functional_owner_name: str
    functional_owner_company: str
    functional_owner_email: str
    functional_owner_phone: str
    technical_owner_name: str
    technical_owner_company: str
    technical_owner_email: str
    technical_owner_phone: str
    developer_name: str
    developer_company: str
    developer_email: str
    developer_phone: str
    fileText: str
