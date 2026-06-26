
import streamlit as st

def render_onboarding_page(onboarding_api, repo_info, repo_content):
    st.title("🌱 Developer Onboarding")
    if st.button("Generate Personalized Roadmap"):
        with st.spinner("Generating roadmap..."):
            roadmap = onboarding_api.get_roadmap(repo_info, repo_content)
            st.markdown(roadmap)
    elif "roadmap" in st.session_state:
        st.markdown(st.session_state.roadmap)
