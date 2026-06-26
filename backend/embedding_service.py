import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2", base_faiss_index_path="faiss_index"):
        self.embeddings = SentenceTransformerEmbeddings(model_name=model_name)
        self.base_faiss_index_path = base_faiss_index_path
        self.vectorstore = None
        self.current_repo_name = None

    def _get_faiss_index_path(self, repo_name):
        return os.path.join(self.base_faiss_index_path, repo_name)

    def create_embeddings(self, source_files, repo_name):
        self.current_repo_name = repo_name
        faiss_index_path = self._get_faiss_index_path(repo_name)
        os.makedirs(faiss_index_path, exist_ok=True)

        documents = []
        for file_data in source_files:
            file_path = file_data["file_path"]
            content = file_data["content"]
            
            # Extract metadata
            file_name = os.path.basename(file_path)
            folder = os.path.dirname(os.path.relpath(file_path, os.path.join("repositories", repo_name)))
            _, extension = os.path.splitext(file_name)
            programming_language = extension.replace(".", "").capitalize() if extension else "Unknown"

            # Create Langchain Document objects with metadata
            doc = Document(
                page_content=content,
                metadata={
                    "source": file_path,
                    "file_name": file_name,
                    "folder": folder,
                    "extension": extension,
                    "programming_language": programming_language,
                }
            )
            documents.append(doc)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,  # Adjusted chunk size to 500-700 tokens
            chunk_overlap=100, # Adjusted overlap for better context
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Split documents into chunks and add chunk number metadata
        chunked_documents = []
        for doc in documents:
            chunks = text_splitter.split_documents([doc])
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_number"] = i + 1
                chunked_documents.append(chunk)

        if chunked_documents:
            self.vectorstore = FAISS.from_documents(chunked_documents, self.embeddings)
            self.vectorstore.save_local(faiss_index_path)
            return self.vectorstore
        return None

    def load_embeddings(self, repo_name):
        self.current_repo_name = repo_name
        faiss_index_path = self._get_faiss_index_path(repo_name)
        if os.path.exists(faiss_index_path):
            self.vectorstore = FAISS.load_local(faiss_index_path, self.embeddings, allow_dangerous_deserialization=True)
            return self.vectorstore
        return None

    def get_retriever(self):
        if self.vectorstore:
            return self.vectorstore.as_retriever(search_kwargs={"k": 7}) # Retrieve top 7 relevant chunks for better context
        return None

    def get_relevant_documents(self, query):
        if self.vectorstore:
            return self.vectorstore.similarity_search(query, k=7) # Retrieve top 7 relevant chunks
        return []
