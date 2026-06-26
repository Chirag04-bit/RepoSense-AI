# 🚀 RepoSense AI

> **AI-Powered Repository Analysis & Developer Onboarding Platform**

RepoSense AI is an AI-powered developer assistant that analyzes GitHub repositories using Google Gemini, LangChain, FAISS, and Retrieval-Augmented Generation (RAG). It helps developers understand unfamiliar codebases within minutes by generating repository summaries, answering repository-specific questions, creating onboarding guides, performing impact analysis, and automatically generating professional README files.

---

# ❗ Problem Statement

Understanding an unfamiliar codebase is one of the biggest challenges for developers.

When joining a new project, developers often spend hours or even days:

- 📂 Exploring hundreds of source files
- 🔍 Searching for the application's entry point
- 🧩 Understanding module relationships
- 📖 Reading incomplete or outdated documentation
- ⚠️ Predicting the impact of code changes
- 🤝 Onboarding without proper guidance

Traditional documentation quickly becomes outdated, making repository exploration slow and inefficient.

---

# 💡 Proposed Solution

RepoSense AI leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and repository analysis to automatically understand a GitHub repository and provide intelligent insights.

The platform enables developers to:

- 🤖 Generate architecture-aware repository summaries
- 💬 Chat with the repository using natural language
- 🌱 Create developer onboarding guides
- ⚡ Perform impact analysis before modifying code
- 📝 Generate professional README documentation
- 📊 Detect technologies and project structure automatically

---

# 🏗️ Solution Overview

RepoSense AI performs the following workflow:

1. 📥 Clone the GitHub repository
2. 📂 Parse the project structure
3. 🔍 Detect technologies, frameworks, databases, and entry points
4. 📄 Extract source code and documentation
5. 🧠 Generate embeddings using Sentence Transformers
6. 📚 Store embeddings in a FAISS Vector Database
7. 🤖 Query Google Gemini using LangChain RAG
8. 📊 Present repository insights through an interactive Streamlit dashboard

---

# ✨ Features

## 📂 Repository Analysis

- Clone any public GitHub repository
- Detect:
  - Programming Language
  - Framework
  - Database
  - Package Manager
  - Build Tool
  - Entry Point
  - Repository Complexity
  - Folder Hierarchy

---

## 🤖 AI Repository Summary

Automatically generates:

- Project Purpose
- Technology Stack
- Overall Architecture
- Folder Structure
- Entry Point
- Main Modules
- Request Flow
- Important Files
- Suggested Reading Order

---

## 💬 Repository Chat (RAG)

Ask questions about any repository using natural language.

---

## 🌱 Developer Onboarding

Generate onboarding documentation for new contributors.

Includes:

- Learning Roadmap
- Module Explanation
- Development Workflow
- Reading Sequence
- Important Files

---

## ⚡ Impact Analysis

Predict the consequences of changing any file before modifying it.

---

## 📝 README Generator

Automatically generates a professional README.md for the repository.

---

# 💬 Example Repository Chat Questions

- Explain this repository.
- What is the overall architecture?
- Which framework is being used?
- Explain the backend folder.
- Where is the application's entry point?
- How does authentication work?
- Which files are responsible for API calls?
- Which file should I read first?
- Explain the request flow.
- Summarize the repository in simple language.

---

# ⚡ Example Impact Analysis Questions

- What happens if I modify `repository_service.py`?
- Which files depend on this module?
- What components will be affected?
- Which APIs will break?
- What should I regression test?
- Suggest a safe refactoring strategy.
- What are the downstream effects of changing this class?
- Which modules import this file?
- Will changing this function affect other components?
- Estimate the risk of modifying this file.

---

# 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| 💻 Language | Python |
| 🎨 Frontend | Streamlit |
| 🤖 LLM | Google Gemini 2.5 Flash |
| 🔗 AI Framework | LangChain |
| 📚 Vector Database | FAISS |
| 🧠 Embeddings | Sentence Transformers |
| 📦 Git Operations | GitPython |
| 📄 Environment | Python Dotenv |

---

# 📂 Project Structure

```text
RepoSense-AI
│
├── api/
│   ├── chat_api.py
│   ├── impact_api.py
│   ├── onboarding_api.py
│   ├── repository_api.py
│   └── summary_api.py
│
├── backend/
│   ├── embedding_service.py
│   ├── impact_service.py
│   ├── onboarding_service.py
│   ├── parser.py
│   ├── rag_service.py
│   ├── repository_service.py
│   ├── summary_service.py
│   ├── utils.py
│   └── faiss_index/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   └── app.py
│
├── repositories/
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Future Scope

- 🔒 Private Repository Support
- 🐳 Docker Deployment
- ☁️ Cloud Deployment
- 📈 Dependency Graph Visualization
- 🧪 Automatic Test Generation
- 🔍 Multi-Repository Comparison
- 📊 Code Quality Dashboard
- 🤝 GitHub Pull Request Review Assistant
- 📝 Automatic Documentation Updates
- ⚙️ CI/CD Integration

---

# ⚙️ Clone & Run

```bash
git clone https://github.com/Chirag04-bit/RepoSense-AI.git

cd RepoSense-AI

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Run the application:

```bash
streamlit run main.py
```

---

