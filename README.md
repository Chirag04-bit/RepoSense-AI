# RepoSense AI - AI Powered Repository Intelligence & Developer Onboarding Assistant

RepoSense AI is a production-quality AI application designed to help developers quickly understand unfamiliar GitHub repositories. It leverages Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) to provide intelligent summaries, answer questions, generate onboarding roadmaps, and analyze the impact of proposed code changes.

This project is built with a clean, modular architecture, making it easy to understand, maintain, and deploy on Streamlit Community Cloud.

## Features

### 1. Repository Import
Users can paste a public GitHub repository URL. The application will:
- Clone the repository.
- Ignore unnecessary folders (e.g., `.git`, `node_modules`, `build`, `dist`, `__pycache__`).
- Read supported source code files.
- Build embeddings using Sentence Transformers.
- Store embeddings in FAISS for efficient retrieval.
- Display key repository information: Name, Main Programming Language, Total Files, Total Folders.

### 2. AI Repository Summary
Generates an intelligent summary explaining:
- Purpose of the repository
- Technologies used
- Overall architecture
- Folder structure
- Important modules
- Entry point

### 3. Repository Chat
Allows users to ask natural language questions about the repository, such as:
- "Explain this repository."
- "Explain the authentication flow."
- "Where is login implemented?"
- "Which file connects to the database?"
- "Explain folder structure."
- "Which APIs are available?"
The system uses RAG with LangChain and Google Gemini, and every response includes relevant file names used as context.

### 4. AI Developer Onboarding Assistant
Generates a personalized learning roadmap for a new developer, dynamically tailored to the repository structure. Example output:

```
Day 1
* Read entry point
* Read configuration
* Understand folder structure

Day 2
* Study routes
* Understand request flow

Day 3
* Study models

Week 2
* Authentication Module

Week 3
* Core Business Logic

Week 4
* Suggested beginner files to modify
```

### 5. AI Change Impact Analyzer
Users can describe a proposed change (e.g., "I want to modify auth.py"). The AI estimates:
- Risk Level (Low, Medium, High)
- Files likely to be affected
- Modules likely to be affected
- Reasoning for the impact assessment
- Suggested implementation order

## Tech Stack

- **Programming Language**: Python
- **Frontend**: Streamlit
- **AI Model**: Google Gemini API
- **Repository Handling**: GitPython
- **RAG Framework**: LangChain
- **Embeddings**: Sentence Transformers
- **Vector Database**: FAISS
- **Environment Variables**: python-dotenv

## Project Structure

```text
reposense-ai/
├── frontend/
│   ├── app.py                 # Streamlit UI only
│   ├── pages/
│   │   ├── repository.py
│   │   ├── chat.py
│   │   ├── onboarding.py
│   │   └── impact.py
│   └── components/
│       ├── sidebar.py
│       ├── cards.py
│       └── chatbox.py
│
├── backend/
│   ├── repository_service.py
│   ├── embedding_service.py
│   ├── rag_service.py
│   ├── summary_service.py
│   ├── onboarding_service.py
│   ├── impact_service.py
│   ├── parser.py
│   └── utils.py
│
├── api/
│   ├── repository_api.py
│   ├── chat_api.py
│   ├── onboarding_api.py
│   ├── impact_api.py
│   └── summary_api.py
│
├── repositories/              # Cloned repositories are stored here
│
├── main.py                    # Application entry point
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
├── README.md                  # Project README
└── .gitignore                 # Files to ignore in Git
```

## File Responsibilities

- **`main.py`**: Responsible for starting the application, initializing the Streamlit app, loading environment variables, and connecting the frontend with the backend. No business logic here.
- **`frontend/`**: Contains only User Interface, Streamlit pages, components, sidebar, buttons, and layout. No AI logic.
- **`backend/`**: Contains repository processing, Git cloning, chunking, embedding generation, FAISS indexing, LangChain integration, Gemini integration, summary generation, onboarding generation, and change impact analysis. No UI code.
- **`api/`**: Contains lightweight wrapper functions that connect the frontend with backend services. No business logic.

## UI Design

The application features a clean, modern, and responsive interface:

- **Sidebar**: Includes a field for GitHub Repository URL and an "Analyze Repository" button.
- **Main Area**: Uses expandable sections for each feature: Repository Information, Repository Summary, Repository Chat, Developer Onboarding, and Change Impact Analyzer.

## Coding Standards

- Modular code
- Easy to understand
- Well commented
- Proper function names
- Type hints where appropriate
- Error handling
- Environment variables for API keys
- No duplicate code

## Deployment

The application is designed for easy deployment on **Streamlit Community Cloud** without requiring Docker or complex configuration. All dependencies are correctly listed in `requirements.txt`.
