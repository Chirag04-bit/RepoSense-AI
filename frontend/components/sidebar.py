
import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.title("🚀 RepoSense AI")
        st.markdown("---")
        repo_url = st.text_input("GitHub Repository URL", placeholder="https://github.com/user/repo")
        analyze_button = st.button("Analyze Repository", use_container_width=True)
        generate_readme_button = st.button("Generate README.md", use_container_width=True)
        st.markdown("---")
        st.markdown("### About")
        st.info("RepoSense AI helps you understand unfamiliar repositories quickly using RAG and LLMs.")
        return repo_url, analyze_button, generate_readme_button
