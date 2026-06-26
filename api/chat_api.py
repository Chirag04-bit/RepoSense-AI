
from backend.rag_service import RAGService
from backend.embedding_service import EmbeddingService

class ChatAPI:
    def __init__(self, repo_name=None):
        self.embedding_service = EmbeddingService()
        if repo_name:
            self.embedding_service.load_embeddings(repo_name)
        self.rag_service = RAGService(self.embedding_service)

    def ask_question(self, question):
        response = self.rag_service.query_repository(question)
        return response
