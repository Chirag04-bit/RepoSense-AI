
import os
from dotenv import load_dotenv

def load_environment_variables():
    load_dotenv()
    # Ensure GOOGLE_API_KEY is loaded
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment variables. Please set it in .env file.")
        # In a real application, you might want to raise an exception or exit

def get_repo_name_from_url(repo_url):
    if not repo_url:
        return ""
    # Handle cases where URL might end with / or .git
    repo_name = repo_url.split("/")[-1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return repo_name
