from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any
import PyPDF2
import io
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import PyPDF2
import io
from llm_reviewer.agent import *
import json
from llm_reviewer.brevity import *
from llm_reviewer.style import *
from llm_reviewer.impact import *
import fitz
import tempfile
from utils import *
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


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


@app.post("/quantification")
async def analyze_quantification(input: TextList):
    return quantification(input.points_to_check)

@app.post("/repetition")
async def analyze_repetition(input: TextList):
    return repetition(input.points_to_check)

@app.post("/weak_verb_checker")
async def check_weak_verbs(input: TextList):
    return weak_verb_checker(input.points_to_check)

@app.post("/verb_tense")
async def check_verb_tense(input: TextList):
    return verb_tense(input.points_to_check)

@app.post("/responsibility")
async def analyze_responsibility(input: TextList):
    return reponsibility(input.points_to_check)

@app.post("/spelling_checker")
async def check_spelling(input: TextList):
    return spelling_checker(input.points_to_check)

@app.post("/resume_length")
async def analyze_resume_length(request: ResumeAnalysisRequest):
    return resume_length(request.text, request.experience)

@app.post("/bullet_point_length")
async def analyze_bullet_point_length(input:TextList):
    return bullet_point_length(input.points_to_check)

@app.post("/total_bullet_list")
async def analyze_total_bullet_list(request: ResumeAnalysisRequest):
    return total_bullet_list(request.text.split('\n'), request.experience)

@app.post("/bullet_points_improver")
async def improve_bullet_points(input: TextList):
    return bullet_points_improver(input.points_to_check)

@app.post("/personal_info")
async def check_personal_info(input:DictInput):
    return personal_info(input.data)

@app.post("/section_checker")
async def check_sections(input:TextList):
    return section_checker(input.points_to_check)

@app.post("/skill_checker")
async def check_skills(request: SkillCheckerRequest):
    return skill_checker(request.hard_skills, request.soft_skills, request.profile)

@app.post("/extract_text_from_pdf")
async def extract_pdf_text(file: UploadFile = File(...)):
    contents = await file.read()
    pdf_file = io.BytesIO(contents)
    return {"text": extract_text_from_pdf(pdf_file)}

@app.post("/extract_structured_data")
async def extract_data(input: TextInput):
    return extract_structured_data(input.cv_text)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)