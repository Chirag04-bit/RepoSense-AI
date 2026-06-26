
import streamlit as st

def render_chat_box(chat_api):
    st.subheader("💬 Repository Chat")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                st.markdown(message["content"])
            else:
                st.markdown(message["explanation"])
                with st.expander("References & Metadata"):
                    st.markdown(f"**Referenced Files:** {', '.join(message['sources'])}")
                    st.markdown(f"**Reasoning:** {message['reasoning']}")
                    st.markdown(f"**Confidence:** {message['confidence']}")
                    st.markdown(f"**Follow-up:** {message['follow_up']}")

    if prompt := st.chat_input("Ask something about the repository..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_api.ask_question(prompt)
                
                explanation = response["ai_explanation"]
                sources = response["referenced_files"]
                reasoning = response["reasoning_for_file_selection"]
                confidence = response["confidence_score"]
                follow_up = response["suggested_follow_up_question"]

                st.markdown(explanation)
                with st.expander("References & Metadata"):
                    st.markdown(f"**Referenced Files:** {', '.join(sources)}")
                    st.markdown(f"**Reasoning:** {reasoning}")
                    st.markdown(f"**Confidence:** {confidence}")
                    st.markdown(f"**Follow-up:** {follow_up}")
                
                st.session_state.messages.append({
                    "role": "assistant", 
                    "explanation": explanation,
                    "sources": sources,
                    "reasoning": reasoning,
                    "confidence": confidence,
                    "follow_up": follow_up
                })
