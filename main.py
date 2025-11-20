import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Inquiry, CaseStudy, JobOpening, TeamMember

app = FastAPI(title="STRNADEL engineering API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "STRNADEL engineering API", "status": "ok"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, "name", None) or "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                response["collections"] = db.list_collection_names()[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

# Utility to convert ObjectId to str for responses
class Doc(BaseModel):
    id: str

# --- Inquiry Endpoints ---
@app.post("/api/inquiries", response_model=Doc)
def create_inquiry(payload: Inquiry):
    try:
        inserted_id = create_document("inquiry", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Case Studies (read-only basic endpoints for frontend showcase) ---
@app.get("/api/case-studies")
def list_case_studies(limit: Optional[int] = 12):
    try:
        docs = get_documents("casestudy", {}, limit or 0)
        # Convert ObjectId
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Jobs (read-only for now) ---
@app.get("/api/jobs")
def list_jobs(limit: Optional[int] = 20):
    try:
        docs = get_documents("jobopening", {}, limit or 0)
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Team (read-only) ---
@app.get("/api/team")
def list_team(limit: Optional[int] = 20):
    try:
        docs = get_documents("teammember", {}, limit or 0)
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
