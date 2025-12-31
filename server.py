from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware

from io import BytesIO
from dotenv import load_dotenv
from supabase import create_client
import os


app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=False,    
    allow_methods=["*"],        
    allow_headers=["*"],        
)

@app.get("/")
async def root():
    return {"messgae":"healthy"}

supabase = create_client(supabase_url=os.getenv("SUPABASE_URL"),supabase_key=os.getenv("SUPABASE_KEY"))

@app.post("/upload-files/")
async def upload(file:UploadFile=File(...)):
    BUCKET = "ResumeInputBucket"
    contents = await file.read()
    response = supabase.storage.from_(BUCKET).upload(
        path = f"{BUCKET}/{file.filename}",
        file = contents,
        file_options = {
            "content_type":"application/pdf",
            "upsert":False
        }
    )
    print(response)
    return {"nothing":"nothing"}

@app.post("/webhook-call")
async def webhook_call(data:dict):
    print(data)
    return {"status":"received"}git 

