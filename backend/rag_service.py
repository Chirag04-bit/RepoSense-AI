import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

class RAGService:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)
        self.qa_chain = None

    def initialize_qa_chain(self):
        retriever = self.embedding_service.get_retriever()
        if not retriever:
            print("Error: Embedding service not initialized or no vectorstore loaded.")
            return

        prompt_template = """You are an experienced software architect AI assistant helping a new developer understand a GitHub repository. Use the following pieces of context from the repository to answer the question at the end. Your answer should be comprehensive, avoid hallucinations, and reference specific files when possible. If the repository does not contain enough information, clearly state that.

Context from repository files:
{context}

Question: {question}

Provide your answer in the following structured format:
AI Explanation: [Your detailed explanation here, referencing file names and their purpose from the context]
Referenced Files: [List of file paths from the context that were most relevant, e.g., file1.py, folder/file2.js]
Reasoning for File Selection: [Briefly explain why these files were relevant to answer the question]
Confidence Score: [Your confidence in the answer, e.g., High, Medium, Low]
Suggested Follow-up Question: [A relevant follow-up question a new developer might ask]
"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt_template)

        self.qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
        )

    def query_repository(self, question):
        if not self.qa_chain:
            self.initialize_qa_chain()
            if not self.qa_chain:
                return {
                    "ai_explanation": "RAG service not properly initialized. Please analyze a repository first.",
                    "referenced_files": [],
                    "reasoning_for_file_selection": "N/A",
                    "confidence_score": "N/A",
                    "suggested_follow_up_question": "N/A"
                }

        result = self.qa_chain({"query": question})
        full_response = result["result"]
        source_documents = result["source_documents"]
        
        # Parse the structured response from the LLM
        ai_explanation = ""
        referenced_files = []
        reasoning_for_file_selection = ""
        confidence_score = ""
        suggested_follow_up_question = ""

        lines = full_response.split("\n")
        current_section = None
        for line in lines:
            if line.startswith("AI Explanation:"):
                current_section = "explanation"
                ai_explanation = line.replace("AI Explanation:", "").strip()
            elif line.startswith("Referenced Files:"):
                current_section = "referenced_files"
                files_str = line.replace("Referenced Files:", "").strip()
                referenced_files = [f.strip() for f in files_str.split(",")] if files_str else []
            elif line.startswith("Reasoning for File Selection:"):
                current_section = "reasoning"
                reasoning_for_file_selection = line.replace("Reasoning for File Selection:", "").strip()
            elif line.startswith("Confidence Score:"):
                current_section = "confidence"
                confidence_score = line.replace("Confidence Score:", "").strip()
            elif line.startswith("Suggested Follow-up Question:"):
                current_section = "follow_up"
                suggested_follow_up_question = line.replace("Suggested Follow-up Question:", "").strip()
            elif current_section == "explanation":
                ai_explanation += "\n" + line.strip()
            elif current_section == "reasoning":
                reasoning_for_file_selection += "\n" + line.strip()
            # Other sections are single line, so no need to append

        # Ensure all source documents are captured, even if LLM misses some in its 'Referenced Files' section
        all_source_files = list(set([doc.metadata["source"] for doc in source_documents]))
        if not referenced_files and all_source_files:
            referenced_files = all_source_files

        return {
            "ai_explanation": ai_explanation,
            "referenced_files": referenced_files,
            "reasoning_for_file_selection": reasoning_for_file_selection,
            "confidence_score": confidence_score,
            "suggested_follow_up_question": suggested_follow_up_question
        }
