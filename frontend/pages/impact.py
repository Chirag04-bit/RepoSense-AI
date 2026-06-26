
import streamlit as st

def render_impact_page(impact_api, repo_content):
    st.title("🔍 Change Impact Analyzer")
    proposed_change = st.text_area("Describe the change you want to make:", placeholder="e.g., I want to modify the authentication logic in auth.py")
    if st.button("Analyze Impact"):
        if proposed_change:
            with st.spinner("Analyzing impact..."):
                analysis = impact_api.get_impact_analysis(repo_content, proposed_change)
                st.markdown(analysis)
        else:
            st.warning("Please describe a change first.")
