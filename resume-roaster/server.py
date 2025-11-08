"""
FastAPI server for Resume Roaster - connects frontend to backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
import shutil
import json

# Import existing modules
from parser import parse_resume
from analyzer import analyze_resume
from roaster import generate_roast_report
from video_generator import generate_video, get_video_dependencies_status, get_available_backgrounds

app = FastAPI(title="Resume Roaster API")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory setup
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# In-memory job storage (use Redis/database in production)
jobs: Dict[str, dict] = {}


class JobStatus(BaseModel):
    job_id: str
    status: str  # pending, analyzing, roasting, generating, completed, failed
    progress: int  # 0-100
    message: str
    video_url: Optional[str] = None
    roast_text: Optional[str] = None
    score: Optional[int] = None
    error: Optional[str] = None


class ProcessingRequest(BaseModel):
    tone: str = "medium"  # gentle, medium, savage
    background_video: str = "subway_surfer"  # subway_surfer, minecraft, fortnite, templerun, satisfying


@app.get("/")
async def root():
    """Health check endpoint"""
    deps = get_video_dependencies_status()
    return {
        "status": "ok",
        "message": "Resume Roaster API is running",
        "video_generation": "enabled" if deps['ready'] else "limited",
        "dependencies": deps,
        "available_backgrounds": get_available_backgrounds()
    }


@app.get("/api/backgrounds")
async def list_backgrounds():
    """
    Get list of available background videos
    """
    return {
        "backgrounds": get_available_backgrounds()
    }


@app.post("/api/upload")
async def upload_resume(
    file: UploadFile = File(...),
    background_video: str = Form("subway_surfer"),
    background_tasks: BackgroundTasks = None
) -> Dict[str, str]:
    """
    Upload a resume file (PDF or DOCX) and start processing
    Returns a job_id to track processing status
    """
    # Validate file type
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF and DOCX files are supported."
        )

    # Validate file size (max 10MB)
    file_content = await file.read()
    file_size = len(file_content)
    if file_size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File too large. Maximum size is 10MB."
        )

    # Generate unique job ID
    job_id = str(uuid.uuid4())

    # Save uploaded file
    file_ext = Path(file.filename).suffix
    upload_path = UPLOAD_DIR / f"{job_id}{file_ext}"

    with open(upload_path, "wb") as f:
        f.write(file_content)

    # Initialize job
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "message": "Resume uploaded successfully",
        "filename": file.filename,
        "upload_path": str(upload_path),
        "background_video": background_video,
        "created_at": datetime.now().isoformat(),
    }

    # Start processing in background
    background_tasks.add_task(process_resume, job_id, str(upload_path), "medium", background_video)

    return {"job_id": job_id, "message": "Upload successful, processing started"}


@app.get("/api/status/{job_id}")
async def get_job_status(job_id: str) -> JobStatus:
    """
    Get the current status of a processing job
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    return JobStatus(**job)


@app.get("/api/result/{job_id}")
async def get_result(job_id: str):
    """
    Get the final result including roast text and video URL
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed yet. Current status: {job['status']}"
        )

    return {
        "job_id": job_id,
        "roast_text": job.get("roast_text"),
        "score": job.get("score"),
        "video_url": job.get("video_url"),
        "issues": job.get("issues", []),
    }


@app.get("/api/video/{job_id}")
async def get_video(job_id: str):
    """
    Stream or download the generated video file
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    video_path = job.get("video_path")

    if not video_path or not Path(video_path).exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"roast_{job_id}.mp4"
    )


async def process_resume(job_id: str, file_path: str, tone: str = "medium", background_video: str = "subway_surfer"):
    """
    Background task to process the resume:
    1. Parse the resume
    2. Analyze for issues
    3. Generate roast using Claude AI
    4. Create brainrot-style video with selected background
    """
    try:
        # Update status: analyzing
        jobs[job_id].update({
            "status": "analyzing",
            "progress": 10,
            "message": "Parsing and analyzing your resume..."
        })
        await asyncio.sleep(0.5)  # Give time for status update

        # Step 1: Parse resume
        resume_data = parse_resume(file_path)

        if not resume_data:
            raise Exception("Failed to parse resume")

        jobs[job_id].update({
            "progress": 30,
            "message": "Resume parsed successfully, analyzing content..."
        })

        # Step 2: Analyze resume
        analysis = analyze_resume(resume_data)

        jobs[job_id].update({
            "status": "roasting",
            "progress": 50,
            "message": "Generating your personalized roast..."
        })

        # Step 3: Generate roast using Claude AI
        roast_output = generate_roast_report(analysis, tone=tone)

        # Parse roast output to extract score and text
        roast_text = roast_output
        score = analysis.get('total_score', 0)

        jobs[job_id].update({
            "status": "generating",
            "progress": 75,
            "message": "Creating your roast video...",
            "roast_text": roast_text,
            "score": score,
            "issues": analysis.get('issues', [])
        })

        # Step 4: Generate video with text-to-speech
        video_path = OUTPUT_DIR / f"{job_id}.mp4"

        # Save roast as JSON for reference
        roast_data_path = OUTPUT_DIR / f"{job_id}_roast.json"
        with open(roast_data_path, "w") as f:
            json.dump({
                "roast_text": roast_text,
                "score": score,
                "issues": analysis.get('issues', [])
            }, f, indent=2)

        # Generate actual brainrot video with selected background
        generate_video(
            roast_text=roast_text,
            score=score,
            output_path=str(video_path),
            issues=analysis.get('issues', []),
            tone=tone,
            background_video=background_video
        )

        # Mark as completed
        jobs[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Roast complete! Your video is ready.",
            "video_url": f"/api/video/{job_id}",
            "video_path": str(video_path)
        })

    except Exception as e:
        jobs[job_id].update({
            "status": "failed",
            "progress": 0,
            "message": "Processing failed",
            "error": str(e)
        })
        print(f"Error processing job {job_id}: {e}")


@app.post("/api/process/{job_id}")
async def trigger_processing(
    job_id: str,
    request: ProcessingRequest,
    background_tasks: BackgroundTasks
):
    """
    Manually trigger processing for an uploaded file
    (Alternative to automatic processing on upload)
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    upload_path = job.get("upload_path")

    if not upload_path or not Path(upload_path).exists():
        raise HTTPException(status_code=404, detail="Uploaded file not found")

    background_tasks.add_task(process_resume, job_id, upload_path, request.tone)

    return {"message": "Processing started", "job_id": job_id}


@app.delete("/api/job/{job_id}")
async def delete_job(job_id: str):
    """
    Delete a job and its associated files
    """
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    # Delete uploaded file
    upload_path = job.get("upload_path")
    if upload_path and Path(upload_path).exists():
        Path(upload_path).unlink()

    # Delete video file
    video_path = job.get("video_path")
    if video_path and Path(video_path).exists():
        Path(video_path).unlink()

    # Remove from jobs
    del jobs[job_id]

    return {"message": "Job deleted successfully"}


if __name__ == "__main__":
    import uvicorn
    print("Starting Resume Roaster API server...")
    print("API will be available at http://localhost:8000")
    print("API docs at http://localhost:8000/docs")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
