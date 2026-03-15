from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from uuid import uuid4

router = APIRouter(prefix="/upload", tags=["Upload"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


router.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:

        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)


        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())


        file_url = f"http://127.0.0.1:8000/uploads/{unique_filename}"

        return JSONResponse(content={"file_url": file_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))