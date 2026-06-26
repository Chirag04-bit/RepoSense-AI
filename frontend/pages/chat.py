
import streamlit as st
from frontend.components.chatbox import render_chat_box

def render_chat_page(chat_api):
    st.title("💬 Chat with Repository")
    render_chat_box(chat_api)
