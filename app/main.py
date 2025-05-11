import os

import streamlit as st

current_dir = os.path.dirname(os.path.abspath(__file__))

document_context_agent_page = st.Page(
    os.path.join(current_dir, "pages", "document_context_agent", "agent.py"),
    url_path="/document_context_agent",
    title="Document Context Agent",
    icon="📖",
)
api_call_agent_page = st.Page(
    os.path.join(current_dir, "pages", "api_call_agent", "agent.py"),
    url_path="/api_call_agent",
    title="API Call Agent",
    icon="🔗",
)
memory_agent_page = st.Page(
    os.path.join(current_dir, "pages", "memory_agent", "agent.py"),
    url_path="/memory_agent",
    title="Memory Agent",
    icon="💾",
)
main_page = st.Page(
    os.path.join(current_dir, "pages", "home.py"),
    title="Main Page",
    url_path="/",
    icon="🎈",
)

pg = st.navigation(
    [main_page, document_context_agent_page, api_call_agent_page, memory_agent_page]
)
pg.run()
