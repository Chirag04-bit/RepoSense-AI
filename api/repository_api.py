
from backend.repository_service import RepositoryService
from backend.embedding_service import EmbeddingService
from backend.utils import get_repo_name_from_url

class RepositoryAPI:
    def __init__(self):
        self.repo_service = RepositoryService()
        self.embedding_service = EmbeddingService()

    def import_repository(self, repo_url):
        repo_name = get_repo_name_from_url(repo_url)
        repo_path = self.repo_service.clone_repository(repo_url)
        if not repo_path:
            return None, "Failed to clone repository."

        repo_info = self.repo_service.get_repository_info(repo_path)
        source_files = self.repo_service.read_source_code_files(repo_path)
        
        # Collect all content for summary and other AI features that need it
        all_content = ""
        for file in source_files:
            all_content += f"\n\n--- File: {file["file_path"]} ---\n{file["content"]}"

        # Create embeddings with metadata
        self.embedding_service.create_embeddings(source_files, repo_name)
        
        return {
            "info": repo_info,
            "all_content": all_content,
            "repo_path": repo_path,
            "repo_name": repo_name
        }, None
