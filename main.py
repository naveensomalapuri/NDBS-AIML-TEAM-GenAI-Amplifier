from fastapi import FastAPI
from routes.resume_routes import router as resume_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

<<<<<<< HEAD
# Mount static files..
=======
# Mount static files
>>>>>>> 6d6f1e6b52e343dabbcf7b6cd4a886b07c02501f
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="templates")

# Include Resume Routes
app.include_router(resume_router)
