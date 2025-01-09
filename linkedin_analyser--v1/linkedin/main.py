from fastapi import FastAPI, Form, HTTPException
import http.client
import urllib.parse
import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# API Keys from .env file
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
X_RAPIDAPI_KEY = os.getenv("X_RAPIDAPI_KEY")
OPEN_AI_KEY = ""  # Add your OpenAI key if needed

# Functions
def get_linkedin_user_details(linkedin_url):
    encoded_url = urllib.parse.quote(linkedin_url, safe='')
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': X_RAPIDAPI_KEY,
        'X-RapidAPI-Host': "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    conn.request("GET", f"/get-linkedin-profile?linkedin_url={encoded_url}&include_skills=false", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

def get_linkedin_posts(linkedin_url):
    encoded_url = urllib.parse.quote(linkedin_url, safe='')
    conn = http.client.HTTPSConnection("fresh-linkedin-profile-data.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': X_RAPIDAPI_KEY,
        'X-RapidAPI-Host': "fresh-linkedin-profile-data.p.rapidapi.com"
    }
    conn.request("GET", f"/get-profile-posts?linkedin_url={encoded_url}&type=posts", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    print("API Response for Posts:", data)  # Log the raw response
    return json.loads(data)


def generate_text(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "x-api-key": f"{OPEN_AI_KEY}",
        "Referer": "YOUR_SITE_URL",
        "X-Title": "YOUR_APP_NAME",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-4-turbo",
        "max_tokens": 4000,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    return response.json()

# FastAPI App
app = FastAPI()

@app.get("/status")
def status():
    return {"message": "LinkedIn Profile Analyzer API is running!"}

@app.post("/analyze")
def analyze_linkedin_profile(linkedin_url: str = Form(...)):
    try:
        # Fetch user details
        user_details = get_linkedin_user_details(linkedin_url)

        if 'data' not in user_details:
            raise HTTPException(status_code=400, detail="Failed to fetch user details. Please check the LinkedIn URL.")

        user_details_no_urls = {
            key: value for key, value in user_details['data'].items()
            if not isinstance(value, str) or 'http' not in value
        }

        # Fetch user posts
        posts_data = get_linkedin_posts(linkedin_url)
        posts = posts_data.get('data', [])

        if not posts:
            raise HTTPException(status_code=404, detail="No posts found or no text available in posts.")
            


        # Generate detailed analysis
        prompt = f"""
        LinkedIn Profile Analysis

        User Summary:
        - Name: {user_details_no_urls.get('name', 'N/A')}
        - Profile Summary: {user_details_no_urls.get('headline', 'N/A')}
        - Profile URL: {linkedin_url}

        Detailed Analysis Request:
        1. Analyze the technical content of the user's posts.
        2. Extract key phrases or important sentences that showcase expertise.
        3. Assess engagement levels of the posts (likes, comments, shares).
        4. Identify trends in discussed topics and alignment with industry trends.
        5. Evaluate community impact and collaborative efforts.
        6.Display everything about the user

        Posts Analysis:
        """
        for i, post in enumerate(posts, 1):
            try:
                prompt += f"\nPost {i}: {post['text']}"
            except KeyError:
                prompt += f"\nPost {i}: [No text available]"

        analysis_results = generate_text(prompt)

        if 'choices' not in analysis_results:
            raise HTTPException(status_code=500, detail="Failed to generate analysis results.")

        return {
            "user_details": user_details_no_urls,
            "posts": posts,
            "analysis_results": [choice['message']['content'] for choice in analysis_results['choices']]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
