
import streamlit as st
from frontend.components.sidebar import render_sidebar
from api.repository_api import RepositoryAPI
from api.summary_api import SummaryAPI
from api.chat_api import ChatAPI
from api.onboarding_api import OnboardingAPI
from api.impact_api import ImpactAPI
from frontend.pages.repository import render_repository_page
from frontend.pages.chat import render_chat_page
from frontend.pages.onboarding import render_onboarding_page
from frontend.pages.impact import render_impact_page

def main():
    st.set_page_config(page_title="RepoSense AI", page_icon="🚀", layout="wide")

    repo_url, analyze_button, generate_readme_button = render_sidebar()

    if "repo_data" not in st.session_state:
        st.session_state.repo_data = None
    if "summary" not in st.session_state:
        st.session_state.summary = None

    if analyze_button and repo_url:
        with st.spinner("Analyzing repository... This might take a minute."):
            repo_api = RepositoryAPI()
            data, error = repo_api.import_repository(repo_url)
            if error:
                st.error(error)
            else:
                st.session_state.repo_data = data
                summary_api = SummaryAPI()
                st.session_state.summary = summary_api.get_summary(data["info"], data["all_content"])
                st.success("Analysis complete!")

    if generate_readme_button and st.session_state.repo_data:
        with st.spinner("Generating README.md..."):
            summary_api = SummaryAPI()
            readme_content = summary_api.generate_readme(st.session_state.repo_data["info"], st.session_state.repo_data["all_content"])
            st.download_button(
                label="Download README.md",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown",
            )
            st.success("README.md generated and ready for download!")
            st.markdown("### Generated README.md Preview")
            st.markdown(readme_content)

    if st.session_state.repo_data:
        tabs = st.tabs(["📊 Repository Info", "💬 Chat", "🌱 Onboarding", "🔍 Impact Analysis"])
        
        with tabs[0]:
            render_repository_page(st.session_state.repo_data["info"], st.session_state.summary)
        
        with tabs[1]:
            chat_api = ChatAPI(repo_name=st.session_state.repo_data["repo_name"])
            render_chat_page(chat_api)
            
        with tabs[2]:
            onboarding_api = OnboardingAPI()
            render_onboarding_page(onboarding_api, st.session_state.repo_data["info"], st.session_state.repo_data["all_content"])
            
        with tabs[3]:
            impact_api = ImpactAPI(repo_name=st.session_state.repo_data["repo_name"])
            render_impact_page(impact_api, st.session_state.repo_data["all_content"])
    else:
        st.write("Please enter a GitHub repository URL in the sidebar to begin.")

if __name__ == "__main__":
    main()
