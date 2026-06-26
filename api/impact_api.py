
from backend.impact_service import ImpactService
from backend.embedding_service import EmbeddingService

class ImpactAPI:
    def __init__(self, repo_name=None):
        self.embedding_service = EmbeddingService()
        if repo_name:
            self.embedding_service.load_embeddings(repo_name)
        self.impact_service = ImpactService(self.embedding_service)

    def get_impact_analysis(self, repository_content, proposed_change):
        analysis = self.impact_service.analyze_change_impact(repository_content, proposed_change)
        return analysis
