import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))


memory_agent_page = st.Page(
    os.path.join(current_dir, "app", "pages", "memory_agent", "streamlit_page.py"),
    url_path="/memory_agent",
    title="Memory Agent",
    icon="💾",
)
academic_research_agent_page = st.Page(
    os.path.join(
        current_dir, "app", "pages", "academic_research_agent", "streamlit_page.py"
    ),
    url_path="/academic_research_agent",
    title="Academic Research Agent",
    icon="🔬",
)
podcast_agent_page = st.Page(
    os.path.join(current_dir, "app", "pages", "podcast_agent", "streamlit_page.py"),
    url_path="/podcast_agent",
    title="Podcast Agent",
    icon="🔗",
)
main_page = st.Page(
    os.path.join(current_dir, "app", "pages", "home.py"),
    title="Main Page",
    url_path="/",
    icon="🎈",
)

pg = st.navigation(
    [
        main_page,
        memory_agent_page,
        academic_research_agent_page,
        podcast_agent_page,
    ]
)

st.session_state.ai_model_id = st.sidebar.selectbox(
    label="AI Model", options=["llama3.1:8b", "qwen3:14b", "deepseek-r1:14b"], index=0
)

pg.run()
