import streamlit as st
from langchain_core.messages import HumanMessage


def get_session_message(session_id:int=None):
    messages=[]
    session_id=session_id or st.session_state.session_id
    session=st.session_state.robot.get_session_history(session_id)
    for message in session.messages[1:]:
        message=("Human",message.content)if isinstance(message,HumanMessage) else ("AI",message.content)
        messages.append(message)
    return messages
def get_all_session_ids():
    return [session_id for session_id in st.session_state.robot.session_data.keys()]

def create_response(question:str,session_id:int=None):
    session_id=session_id or st.session_state.session_id
    response=st.session_state.robot.stream(question,session_id)
    return response

def start_session():
    st.session_state.session_id=max(st.session_state.robot.session_data.keys(),default=0)+1
    st.session_state.robot.get_session_history(st.session_state.session_id)

def continue_session(session_id:int):
    st.session_state.session_id=session_id

def delete_session(session_id:int):
    chathistory=st.session_state.robot.session_data.pop(session_id)
    chathistory.clear()
    st.session_state.session_id=max(st.session_state.robot.session_data.keys(),default=1)