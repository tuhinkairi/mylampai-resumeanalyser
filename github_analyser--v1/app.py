from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

app = FastAPI()

# Request model for GitHub username
class UsernameRequest(BaseModel):
    username: str

# Agent class for Generative AI interaction
class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append(SystemMessage(content=self.system))
    
    def __call__(self, message):
        self.messages.append(HumanMessage(content=message))
        result = self.execute()
        self.messages.append(AIMessage(content=result))
        return result
    
    def execute(self):
        chat = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3, convert_system_message_to_human=True)
        result = chat.invoke(self.messages)
        return result.content

# GitHub Info Aggregator class
class GitHubInfo:
    def __init__(self, username):
        self.username = username
        self.user_url = f'https://api.github.com/users/{self.username}'
        self.repo_url = f'https://api.github.com/users/{self.username}/repos'

    def get_user_info(self):
        try:
            user_data_from_github = requests.get(self.user_url).json()
            data_needed = [
                'name', 'type', 'company', 'blog', 'location', 'email', 'public_repos', 'followers'
            ]
            return {k: v for k, v in user_data_from_github.items() if k in data_needed}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching user info: {e}")

    def get_repos_info(self):
        try:
            repos = requests.get(self.repo_url).json()
            if isinstance(repos, list):
                repo_stats = []
                data_needed = [
                    'name', 'html_url', 'description', 'forks', 'open_issues', 'language', 'git_url'
                ]
                for repo in repos:
                    if isinstance(repo, dict):
                        repo_data = {k: repo.get(k, 'N/A') for k in data_needed}

                        # Fetch and analyze README
                        readme_url = f'https://api.github.com/repos/{self.username}/{repo_data["name"]}/readme'
                        try:
                            readme_response = requests.get(readme_url).json()
                            readme_content = readme_response.get('content', None)
                            if readme_content:
                                bot = Agent("Analyze the README content of a GitHub repository.")
                                analysis_result = bot(readme_content)
                                repo_data['readme_analysis'] = analysis_result
                            else:
                                repo_data['readme_analysis'] = "No README found."
                        except Exception:
                            repo_data['readme_analysis'] = "Error analyzing README."

                        repo_stats.append(repo_data)
                return repo_stats
            else:
                return []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching repositories: {e}")

    def get_commit_info(self, repo_name):
        try:
            commit_url = f'https://api.github.com/repos/{self.username}/{repo_name}/commits'
            commits = requests.get(commit_url).json()
            if isinstance(commits, list):
                return [
                    {
                        'sha': commit.get('sha', 'N/A'),
                        'message': commit.get('commit', {}).get('message', 'N/A'),
                        'author': commit.get('commit', {}).get('author', {})
                    }
                    for commit in commits[:5]
                ]
            return []
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching commit stats: {e}")

@app.post("/github_analysis")
def analyze_github(request: UsernameRequest):
    github = GitHubInfo(request.username)

    # Fetch user info
    user_info = github.get_user_info()

    # Fetch repositories and analyze README
    repos_info = github.get_repos_info()

    # Fetch commit info for the first repository
    commit_info = []
    if repos_info:
        first_repo_name = repos_info[0]['name']
        commit_info = github.get_commit_info(first_repo_name)

    return {
        "user_info": user_info,
        "repositories": repos_info,
        "commits": commit_info
    }

