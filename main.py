from robot import Robot
from chroma import MyChroma
import funcs
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
if 'started' not in st.session_state:
    st.session_state.started = True
    st.session_state.chroma = MyChroma.from_folder('./files/rag','rag_collection','./files/docs')
    st.session_state.robot = Robot({"model":'deepseek-chat'},st.session_state.chroma.as_retriever(k=3))
    st.session_state.session_id=1

def init_interface():
    st.set_page_config(page_title="Medical Chatbot",layout="wide")
    st.title("Molly 医疗精灵")
    #显示消息记录
    messages=funcs.get_session_message()
    for message in messages:
        role,content=message
        with st.chat_message(role):
            st.write(content)

    #实现聊天功能
    question=st.chat_input("请输入问题提问....")
    if question is not None:
        response=funcs.create_response(question)
        st.chat_message("Human").write(question)
        st.chat_message("AI").write_stream(response)

    with st.sidebar:
        st.header(f"当前对话ID:{st.session_state.session_id}")
        st.button("开始新对话",on_click=funcs.start_session)
        for session_id in funcs.get_all_session_ids():
            with st.expander(f"对话ID:{session_id}"):
                col1,col2=st.columns(2)
                col1.button("继续对话",on_click=funcs.continue_session,args=(session_id,),key=f"Restart={session_id}")
                col2.button("删除对话",on_click=funcs.delete_session,args=(session_id,),key=f"Delete={session_id}")
if __name__ == '__main__':
    init_interface()