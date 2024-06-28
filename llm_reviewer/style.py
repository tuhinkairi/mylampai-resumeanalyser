import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agent import *
import json

def personal_info(personal_info):
    personal_info_prompt = """
    You are analyzing Personal Information data from a resume. Your tasks are:

Remove any key-value pairs where the value is null.
Verify the presence of essential resume elements:

Full name
Location (city and/or state)
Key contact details (email address, phone number)
Professional profile links (LinkedIn, GitHub, or other relevant profiles)


Identify any irrelevant or potentially problematic personal information.

If you find irrelevant or problematic information, output a JSON object with this structure:
{
  irrelevant_item: "Reason why this is irrelevant or problematic"
}
Examples of irrelevant or problematic information might include:

Sensitive personal details (e.g., age, marital status, religion)
Excessive or unnecessary information
Outdated contact methods

If no irrelevant information is found, return an empty JSON object:
{}
Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.
    """.strip()
    personal_info_checker = Agent(personal_info_prompt)
    personal_info_resp = personal_info_checker(str(personal_info))
    json_file = json.loads(personal_info_resp.strip().strip('```json').strip('```'))
    return json_file

def section_checker(sections):
    section_checker = """
   You are an experienced HR professional at a Fortune 500 company, renowned for your expertise in resume evaluation. Your task is to analyze the sections of a resume for completeness and relevance.
    Given a list of sections from a resume, you will:

    Identify any irrelevant sections that don't belong in a professional resume.
    Note any critical sections that are missing.

    Essential sections typically include:

    Contact Information
    Professional Summary or Objective
    Work Experience or Projects 
    Education
    Skills
    Extra-curriculars
    Coursework
    (Optional but often valuable) Achievements or Projects

    If you find irrelevant sections or notice missing critical sections, provide your analysis in a JSON format as follows:
    {
    "Irrelevant Section Name": "Reason why this section is inappropriate or unnecessary",
    "Missing Section Name": "Explanation of why this section is important and should be included"
    }
    Examples:

    Irrelevant: "Hobbies" might be irrelevant unless directly related to the job.
    Missing: "Work Experience" is critical for most professional resumes.

    If all sections are appropriate and no critical sections are missing, return an empty JSON object:
        {}
    Ensure your response begins with "```json" and ends with "```" to properly format the JSON output.
    Remember, your goal is to ensure the resume sections are professional, relevant, and complete for a competitive job market.
        """.strip()
    section_checker = Agent(section_checker)
    section_resp = section_checker(str(sections))
    json_file = json.loads(section_resp.strip().strip('```json').strip('```'))
    return json_file

def skill_checker(hard_skills,soft_skills,profile="Full Stack Web Development"):
    skill_checker = """
    YOU are HR of a FORTUNE 500 Company who is very good at judging the RESUME.
    You will be provided with Skills of a person from a RESUME for profile if {}.
    You have to judge both the HARD SKills and SOFT Skills and suggest other HARD and SOFT SKills that can be added in the RESUME to increase IMPACT of RESUME for the said profile
    output a json object starting with '```json' and trailing with '```' containing key as "HARD" with value a list of new hard skill that can be added for the given profile, and another key "SOFT" with value a list of new soft skill that can be added for the given profile
    """.format(profile)

    skill_checker_bot = Agent(skill_checker)
    skill_checker_resp = skill_checker_bot("HARD SKILLS"+ str(hard_skills)+ "SOFT SKILLS"+str(soft_skills))
    json_file = json.loads(skill_checker_resp.strip().strip('```json').strip('```'))
    return json_file