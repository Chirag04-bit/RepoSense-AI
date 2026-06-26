from backend.summary_service import SummaryService


class SummaryAPI:
    def __init__(self):
        self.summary_service = SummaryService()

    def get_summary(self, repo_info, all_files_content):
        return self.summary_service.generate_summary(
            repo_info,
            all_files_content,
        )

    def generate_readme(self, repo_info, all_files_content):
        return self.summary_service.generate_readme(
            repo_info,
            all_files_content,
        )