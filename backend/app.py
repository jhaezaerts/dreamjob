from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from azure.storage.blob import BlobServiceClient
import json
import os
import azure.core.exceptions
from dotenv import load_dotenv

load_dotenv()  # Add this line before accessing env variables

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Storage settings
CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "dreamjobs"
BLOB_NAME = "jobs.json"

blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)

# Ensure container exists
try:
    container_client = blob_service_client.create_container(CONTAINER_NAME)
except azure.core.exceptions.ResourceExistsError:
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)

class DreamJob(BaseModel):
    name: str
    job: str

def get_jobs_from_blob():
    try:
        blob_client = container_client.get_blob_client(BLOB_NAME)
        data = blob_client.download_blob().readall()
        return json.loads(data)
    except azure.core.exceptions.ResourceNotFoundError:
        return []

def save_jobs_to_blob(jobs):
    blob_client = container_client.get_blob_client(BLOB_NAME)
    blob_client.upload_blob(json.dumps(jobs), overwrite=True)

@app.get("/jobs")
def get_jobs():
    return get_jobs_from_blob()

@app.post("/submit")
def submit_job(dream_job: DreamJob):
    jobs = get_jobs_from_blob()
    jobs.append(dream_job.model_dump())
    save_jobs_to_blob(jobs)
    return {"message": "Dream job submitted!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
