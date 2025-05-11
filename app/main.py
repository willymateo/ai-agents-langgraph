import streamlit as st
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

document_context_agent_page = st.Page(os.path.join(current_dir,"pages","document_context_agent","agent.py"), title="Document Context Agent", icon="📖", url_path="/document_context_agent")
api_call_agent_page = st.Page(os.path.join(current_dir,"pages","api_call_agent","agent.py"), title="API Call Agent", icon="🔗",  url_path="/api_call_agent")
memory_agent_page = st.Page(os.path.join(current_dir,"pages","memory_agent","agent.py"), title="Memory Agent", icon="💾", url_path="/memory_agent")
main_page = st.Page(os.path.join(current_dir,"pages","home.py"), title="Main Page", icon="🎈", url_path="/")

pg = st.navigation([main_page,document_context_agent_page, api_call_agent_page, memory_agent_page])
pg.run()
