from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any
import io
import logging
import os
import sys
from app.llm_reviewer.agent import *
from app.llm_reviewer.brevity import *
from app.llm_reviewer.style import *
from app.llm_reviewer.impact import *
from app.utils.utils import *

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Pydantic models
class ResumeAnalysisRequest(BaseModel):
    text: str
    experience: str = "FRESHERS"

class TextList(BaseModel):
    points_to_check: List[str]

class TextInput(BaseModel):
    cv_text: str

class DictInput(BaseModel):
    data: Dict[str, Any]

class SkillCheckerRequest(BaseModel):
    hard_skills: List[str]
    soft_skills: List[str]
    profile: str = "Full Stack Web Development"

# Endpoint to extract text from PDF
@app.post("/extract_text_from_pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        pdf_file = io.BytesIO(contents)
        pdf_data = extract_text_from_pdf(pdf_file)
        return {"message": pdf_data}
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from PDF")


# Endpoint to extract structured data from text
@app.post("/extract_structured_data")
async def extract_data(input: TextInput):
    try:
        return {"message": extract_structured_data(input.cv_text)}
    except Exception as e:
        logger.error(f"Error extracting structured data: {e}")
        raise HTTPException(status_code=500, detail="Error extracting structured data")

# Endpoint for quantification analysis
@app.post("/quantification")
async def analyze_quantification(data:DictInput):
    try:
        input = "\n".join(data["Description"])
        return {"message": quantification(input)}
    except Exception as e:
        logger.error(f"Error analyzing quantification: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing quantification")

# Endpoint for repetition analysis
@app.post("/repetition")
async def analyze_repetition(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": repetition(input)}
    except Exception as e:
        logger.error(f"Error analyzing repetition: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing repetition")

# Endpoint for weak verb checking
@app.post("/weak_verb_checker")
async def check_weak_verbs(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": weak_verb_checker(input)}
    except Exception as e:
        logger.error(f"Error checking weak verbs: {e}")
        raise HTTPException(status_code=500, detail="Error checking weak verbs")

# Endpoint for verb tense checking
@app.post("/verb_tense")
async def check_verb_tense(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": verb_tense(input)}
    except Exception as e:
        logger.error(f"Error checking verb tense: {e}")
        raise HTTPException(status_code=500, detail="Error checking verb tense")

# Endpoint for responsibility analysis
@app.post("/responsibility")
async def analyze_responsibility(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": responsibility(input)}
    except Exception as e:
        logger.error(f"Error analyzing responsibility: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing responsibility")

# Endpoint for spelling checking
@app.post("/spelling_checker")
async def check_spelling(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": spelling_checker(input)}
    except Exception as e:
        logger.error(f"Error checking spelling: {e}")
        raise HTTPException(status_code=500, detail="Error checking spelling")

# Endpoint for resume length analysis
@app.post("/resume_length")
async def analyze_resume_length(request: ResumeAnalysisRequest):
    try:
        return {"message": resume_length(request.text, request.experience)}
    except Exception as e:
        logger.error(f"Error analyzing resume length: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing resume length")

# Endpoint for bullet point length analysis
@app.post("/bullet_point_length")
async def analyze_bullet_point_length(data):
    try:
        return {"message": bullet_point_length(input.points_to_check)}
    except Exception as e:
        logger.error(f"Error analyzing bullet point length: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing bullet point length")

# Endpoint for total bullet list analysis
@app.post("/total_bullet_list")
async def analyze_total_bullet_list(cv_data,experience):
    try:
        return {"message": total_bullet_list(cv_data,experience)}
    except Exception as e:
        logger.error(f"Error analyzing total bullet list: {e}")
        raise HTTPException(status_code=500, detail="Error analyzing total bullet list")

# Endpoint to improve bullet points
@app.post("/bullet_points_improver")
async def improve_bullet_points(data):
    try:
        input = "\n".join(data["Description"])
        return {"message": bullet_points_improver(input)}
    except Exception as e:
        logger.error(f"Error improving bullet points: {e}")
        raise HTTPException(status_code=500, detail="Error improving bullet points")

# Endpoint for personal info checking
@app.post("/personal_info")
async def check_personal_info(data):
    try:
        input = "\n".join(data["Personal Information"])
        return {"message": personal_info(input)}
    except Exception as e:
        logger.error(f"Error checking personal info: {e}")
        raise HTTPException(status_code=500, detail="Error checking personal info")

# Endpoint for section checking
@app.post("/section_checker")
async def check_sections(data):
    try:
        input = "\n".join(data["Sections"])
        return {"message": section_checker(input)}
    except Exception as e:
        logger.error(f"Error checking sections: {e}")
        raise HTTPException(status_code=500, detail="Error checking sections")

# Endpoint for skill checking
@app.post("/skill_checker")
async def check_skills(data, profile):
    try:
        hard_skills = data["Skills"]["HARD"]
        soft_skills = data["Skills"]["SOFT"]
        profile = profile
        return {"message": skill_checker(hard_skills, soft_skills, profile)}
    except Exception as e:
        logger.error(f"Error checking skills: {e}")
        raise HTTPException(status_code=500, detail="Error checking skills")
