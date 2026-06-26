
import streamlit as st

def render_repo_info_card(info):
    st.subheader("📊 Repository Information")
    
    # Calculate Repository Complexity
    complexity = "Small"
    if info["total_files"] > 100 or info["total_folders"] > 20 or info["folder_hierarchy"].count('\n') > 50:
        complexity = "Large"
    elif info["total_files"] > 30 or info["total_folders"] > 10 or info["folder_hierarchy"].count('\n') > 20:
        complexity = "Medium"
    
    st.markdown(f"**Repository Complexity:** `{complexity}`")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Repository Name", info["repo_name"])
    with col2:
        st.metric("Primary Language", info["main_language"])
    with col3:
        st.metric("Framework", info["framework"])

    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Database", info["database"])
    with col5:
        st.metric("ORM", info["orm"])
    with col6:
        st.metric("Auth Library", info["auth_library"])

    col7, col8, col9 = st.columns(3)
    with col7:
        st.metric("Build Tool", info["build_tool"])
    with col8:
        st.metric("Testing Framework", info["testing_framework"])
    with col9:
        st.metric("Package Manager", info["package_manager"])

    col10, col11, col12 = st.columns(3)
    with col10:
        st.metric("Entry Point", info["entry_point"])
    with col11:
        st.metric("Total Files", info["total_files"])
    with col12:
        st.metric("Total Folders", info["total_folders"])

    st.metric("README Present", "Yes" if info["readme_present"] else "No")

    with st.expander("Configuration Files"):
        if info["config_files"]:
            for cfg_file in info["config_files"]:
                st.markdown(f"- `{cfg_file}`")
        else:
            st.info("No specific configuration files detected.")

    with st.expander("Folder Hierarchy (Top 3 Levels)"):
        st.code(info["folder_hierarchy"], language="text")

    with st.expander("Mermaid Diagram (Folder Structure)"):
        st.code(info["mermaid_diagram"], language="mermaid")
        st.info("You can copy this Mermaid code and paste it into an online Mermaid editor (e.g., mermaid.live) to visualize the repository structure.")
