import os

import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))

document_context_agent_page = st.Page(
    os.path.join(
        current_dir, "app", "pages", "document_context_agent", "streamlit_page.py"
    ),
    url_path="/document_context_agent",
    title="Document Context Agent",
    icon="📖",
)
api_call_agent_page = st.Page(
    os.path.join(current_dir, "app", "pages", "api_call_agent", "streamlit_page.py"),
    url_path="/api_call_agent",
    title="API Call Agent",
    icon="🔗",
)
memory_agent_page = st.Page(
    os.path.join(current_dir, "app", "pages", "memory_agent", "streamlit_page.py"),
    url_path="/memory_agent",
    title="Memory Agent",
    icon="💾",
)
main_page = st.Page(
    os.path.join(current_dir, "app", "pages", "home.py"),
    title="Main Page",
    url_path="/",
    icon="🎈",
)

pg = st.navigation(
    [main_page, document_context_agent_page, api_call_agent_page, memory_agent_page]
)
pg.run()
