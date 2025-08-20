import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3
from langchain_community.utilities import SQLDatabase
from langchain.agents import create_sql_agent, AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_groq import ChatGroq

# Page config
st.set_page_config(page_title="Langchain: Chat with SQL", page_icon="🧠")
st.title("Langchain: Chat with SQL")

# Database mode
radio_opt = ["Use SQLite 3 Database - Student.db", "Connect to your SQL Database"]
selected_opt = st.sidebar.radio("Choose the DB you want to chat with", options=radio_opt)

LOCALDB = "LOCALDB"
MYSQL = "MYSQL"

if selected_opt == radio_opt[0]:
    db_mode = LOCALDB
else:
    db_mode = MYSQL
    mysql_host = st.sidebar.text_input("MySQL Host", value="localhost")
    mysql_user = st.sidebar.text_input("MySQL User", value="root")
    mysql_password = st.sidebar.text_input("MySQL Password", type="password")
    mysql_db = st.sidebar.text_input("MySQL Database", value="project")

# API key
api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.info("Please enter the Groq API key.")
    st.stop()

llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

@st.cache_resource(ttl="2h")
def configure_db():
    if db_mode == LOCALDB:
        db_file = Path(__file__).parent / "imdb.db"
        if not db_file.exists():
            st.error(f"❌ SQLite DB not found at {db_file}")
            st.stop()
        engine = create_engine(f"sqlite:///{db_file}")
    else:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("❌ Please provide all MySQL connection details.")
            st.stop()
        engine = create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}")
    return SQLDatabase(engine)

db = configure_db()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
)

# Session history
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_prompt = st.chat_input("Ask anything from the database...")

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").write(user_prompt)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_prompt, callbacks=[streamlit_callback])
        except Exception as e:
            response = f"❌ Error: {e}"
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
