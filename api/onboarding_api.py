
from backend.onboarding_service import OnboardingService

class OnboardingAPI:
    def __init__(self):
        self.onboarding_service = OnboardingService()

    def get_roadmap(self, repo_info, all_files_content):
        roadmap = self.onboarding_service.generate_onboarding_roadmap(repo_info, all_files_content)
        return roadmap
