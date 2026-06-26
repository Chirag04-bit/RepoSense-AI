
import streamlit as st
from frontend.components.cards import render_repo_info_card

def render_repository_page(repo_info, summary):
    st.title("📂 Repository Analysis")
    
    # Heuristic for repository complexity
    complexity = "Low"
    if repo_info["total_files"] > 100 or len(repo_info["config_files"]) > 10:
        complexity = "High"
    elif repo_info["total_files"] > 30 or len(repo_info["config_files"]) > 5:
        complexity = "Medium"
    
    st.markdown(f"**Repository Complexity:** `{complexity}`")
    
    render_repo_info_card(repo_info)
    
    st.markdown("---")
    st.subheader("📝 Repository Summary")
    st.markdown(summary)
