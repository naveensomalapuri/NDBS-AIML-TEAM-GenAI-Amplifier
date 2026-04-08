import os
import json
import logging
import aiofiles

from services.model import openmodel

logger = logging.getLogger(__name__)

RESUME_DIR = "resumes_data"
os.makedirs(RESUME_DIR, exist_ok=True)


def generate_resume(client_problem: str, client_name: str) -> dict:
    response = openmodel(client_problem, client_name)
    if response is None:
        logger.error("No response received from openmodel")
        return {}
    return response


async def save_resume(resume_data: dict) -> str:
    try:
        os.makedirs(RESUME_DIR, exist_ok=True)
        client_name = resume_data.get("client_name", "unknown_client").replace(" ", "_")
        file_name = f"{client_name}.json"
        file_path = os.path.join(RESUME_DIR, file_name)

        if os.path.exists(file_path):
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            existing_data = json.loads(content)
            if not isinstance(existing_data, list):
                raise ValueError(f"File {file_name} does not contain a list.")
            existing_data.append(resume_data)
        else:
            resume_data["file_name"] = file_name
            existing_data = [resume_data]

        async with aiofiles.open(file_path, "w") as f:
            await f.write(json.dumps(existing_data, indent=4))

        return file_name
    except Exception as e:
        logger.error("Error saving resume to file: %s", e)
        return None


async def get_all_resumes() -> list:
    resumes = []
    try:
        for file_name in os.listdir(RESUME_DIR):
            file_path = os.path.join(RESUME_DIR, file_name)
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            resumes.append(json.loads(content))
    except Exception as e:
        logger.error("Error reading resumes from file: %s", e)
    return resumes


async def view_resume(resume_name: str) -> dict:
    try:
        for file_name in os.listdir(RESUME_DIR):
            file_path = os.path.join(RESUME_DIR, file_name)
            async with aiofiles.open(file_path, "r") as f:
                content = await f.read()
            resume_data = json.loads(content)
            generated_resume = resume_data[0].get("generated_resume", {})
            if generated_resume.get("client_name") == resume_name:
                return resume_data
        return {"error": "RICEF not found"}
    except Exception as e:
        logger.error("Error reading RICEF file: %s", e)
        return {"error": str(e)}
