
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

class SummaryService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

    def generate_summary(self, repo_info, all_files_content):
        prompt_template = """You are an experienced software architect AI assistant. Based on the following repository analysis and content, generate a structured and intelligent summary. The summary should feel like a software architect's first impression of the repository.
    
    
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

Generate a structured summary containing the following sections:

### Project Purpose
[Explain the main goal and functionality of the repository]

### Technology Stack
[List primary programming language, framework, database, and other significant technologies detected]

### Overall Architecture
[Describe the high-level structure and design patterns, e.g., MVC, microservices, monolithic]

### Entry Point
[Identify the main entry point and explain its role]

### Folder Structure
[Describe the organization of directories and their purpose, referencing the provided hierarchy]

### Main Modules
[Highlight important modules or sub-systems and their responsibilities]

### Request Flow (if applicable)
[Outline how a typical request or operation flows through the application]

### Important Files
[List critical files beyond the entry point and explain their significance]

### Suggested Files to Read First
[Recommend a few files for a new developer to start reading to quickly grasp the project]

Intelligent Summary:"""
        
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

        summary = chain.run(
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
        return summary
    
    
    def generate_readme(self, repo_info, all_files_content):
        prompt_template = """
You are an expert software engineer.

Generate a professional README.md in Markdown for the following repository.

Repository Name:
{repo_name}

Primary Language:
{main_language}

Framework:
{framework}

Database:
{database}

ORM:
{orm}

Authentication:
{auth_library}

Build Tool:
{build_tool}

Testing Framework:
{testing_framework}

Entry Point:
{entry_point}

Folder Structure:
{folder_hierarchy}

Repository Content:
{all_files_content}

Generate a README.md containing:

# {repo_name}

## Overview

## Features

## Technology Stack

## Project Structure

## Installation

## Usage

## Contributing

## License
"""

        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=[
                "repo_name",
                "main_language",
                "framework",
                "database",
                "orm",
                "auth_library",
                "build_tool",
                "testing_framework",
                "entry_point",
                "folder_hierarchy",
                "all_files_content",
            ],
        )

        chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
        )

        if len(all_files_content) > 10000:
            all_files_content = (
                all_files_content[:10000]
                + "\n... (content truncated)"
            )

        readme = chain.run(
            repo_name=repo_info["repo_name"],
            main_language=repo_info["main_language"],
            framework=repo_info["framework"],
            database=repo_info["database"],
            orm=repo_info["orm"],
            auth_library=repo_info["auth_library"],
            build_tool=repo_info["build_tool"],
            testing_framework=repo_info["testing_framework"],
            entry_point=repo_info["entry_point"],
            folder_hierarchy=repo_info["folder_hierarchy"],
            all_files_content=all_files_content,
        )

        return readme
