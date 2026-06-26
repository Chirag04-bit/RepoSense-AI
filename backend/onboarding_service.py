import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

class OnboardingService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    def generate_onboarding_roadmap(self, repo_info, all_files_content):
        prompt_template = """You are an experienced software architect AI assistant. Based on the following repository analysis and content, create a personalized and structured onboarding roadmap for a new developer. The roadmap should adapt automatically according to repository size and architecture, and include specific files to read, learning goals, and estimated times.

Repository Analysis:
- Repository Name: {repo_name}
- Primary Language: {main_language}
- Framework: {framework}
- Database: {database}
- ORM: {orm}
- Authentication Library: {auth_library}
- Build Tool: {build_tool}
- Testing Framework: {testing_framework}
- Entry Point: {entry_point}
- Total Files: {total_files}
- Total Folders: {total_folders}
- README Present: {readme_present}
- Package Manager: {package_manager}
- Configuration Files: {config_files}
- Folder Hierarchy (top 3 levels):
{folder_hierarchy}

Repository Content (snippets from various files for context):
{all_files_content}

Generate a personalized learning roadmap in the following structured format, adapting to the repository's complexity and size:

### Day 1
* Files to read: [e.g., {entry_point}, README.md]
* Learning Goal: [e.g., Understand the project's main entry point and overall purpose]
* Estimated Time: [e.g., 2-3 hours]

### Day 2
* Files to read: [e.g., relevant_module/routes.py, relevant_module/controllers.py]
* Learning Goal: [e.g., Grasp the request flow and how different components interact]
* Estimated Time: [e.g., 3-4 hours]

### Week 1 (or Day 3-5, depending on complexity)
* Files to read: [e.g., core_business_logic/models.py, core_business_logic/services.py]
* Learning Goal: [e.g., Dive into the core business logic and data models]
* Estimated Time: [e.g., 5-8 hours]

### Week 2 (if applicable)
* Module: Authentication Module
* Files to read: [e.g., auth/auth_service.py, auth/middleware.py]
* Learning Goal: [e.g., Understand user authentication and authorization mechanisms]
* Estimated Time: [e.g., 4-6 hours]

### Week 3 (if applicable)
* Module: Core Business Logic (Advanced)
* Files to read: [e.g., complex_feature/processor.py, complex_feature/utils.py]
* Learning Goal: [e.g., Deep dive into a specific complex feature or domain]
* Estimated Time: [e.g., 6-10 hours]

### Suggested Beginner Files to Modify
* [e.g., tests/test_example.py (for adding a new test)]
* [e.g., docs/usage.md (for updating documentation)]

### Suggested Beginner Tasks
* [e.g., Add a new small feature (e.g., a new API endpoint or UI element)]
* [e.g., Refactor a small utility function]

Personalized Learning Roadmap:"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=[
                "repo_name", "main_language", "framework", "database", "orm",
                "auth_library", "build_tool", "testing_framework", "entry_point",
                "total_files", "total_folders", "readme_present", "package_manager",
                "config_files", "folder_hierarchy", "all_files_content"
            ]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)

        # Truncate content if it's too long for the LLM context window
        max_length = 10000  # Approximate token limit for Gemini-pro, adjust as needed
        if len(all_files_content) > max_length:
            all_files_content = all_files_content[:max_length] + "\n... (content truncated)"

        roadmap = chain.run(
            repo_name=repo_info["repo_name"],
            main_language=repo_info["main_language"],
            framework=repo_info["framework"],
            database=repo_info["database"],
            orm=repo_info["orm"],
            auth_library=repo_info["auth_library"],
            build_tool=repo_info["build_tool"],
            testing_framework=repo_info["testing_framework"],
            entry_point=repo_info["entry_point"],
            total_files=repo_info["total_files"],
            total_folders=repo_info["total_folders"],
            readme_present=repo_info["readme_present"],
            package_manager=repo_info["package_manager"],
            config_files=", ".join(repo_info["config_files"]),
            folder_hierarchy=repo_info["folder_hierarchy"],
            all_files_content=all_files_content
        )
        return roadmap
