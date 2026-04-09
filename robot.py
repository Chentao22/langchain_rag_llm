import os
import sqlite3
from langchain_community.chat_message_histories.sql import SQLChatMessageHistory
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
class Robot:
    system_prompt="""
    你是一个名为Molly的医学专家，\
    对于用户提问的医学相关问题，你需要按照给出的参考文献资料对问题进行回答。\
    你的问题需要按照以下步骤：\
        1.分析用户问题、对话历史以及参考文献，判断参考资料的哪些内容可以解答用户的问题，并将这一过程进行说明。
        2.如果参考文献可以解答用户的问题，则根据文献内容对问题进行解答。
        3.如果参考文献没有可以解答用户问题的内容，则建议用户咨询专业人士寻求帮助，不要自行发挥。
    你的回答需要注意一下几点：
        4.保证你的回答是清晰的、明确的。对于有参考资料的结论，明确指出参考资料的来源和标题等。\
        5.结合用户的对话历史，分析用户的问题意图。但不要复述问题，不要使用“用户”来称呼！
        6.回复用户时，使用对话的口吻，有礼貌地称呼用户为“您”，不要使用“用户”来称呼！
        7.如果用户的问题与医学无关，判断用户的目的，并温柔地提示其回到医学话题。
        """
    greeting_prompt="你好！我是Molly医疗精灵，专注于解决你的医疗问题。请问你需要什么帮助？"
    prompt_template="##用户问题：{input}\n\n参考资料：\n\n##本地知识库：{rag_results}\n\n##对话历史：{chat_history}"
    def __init__(self,model_config:dict,retriever=None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.model=ChatOpenAI( api_key=self.api_key,
                               base_url=self.api_base,
                               **model_config)
        self.prompt=ChatPromptTemplate.from_messages([("human",self.prompt_template)])
        #带记忆的AI
        self.with_message_history=RunnableWithMessageHistory(self.prompt|self.model,get_session_history=self.get_session_history,input_messages_key="input",history_messages_key="chat_history")

        if retriever is None:
            retriever=RunnableLambda(lambda x:"")

        self.chain={"input":RunnablePassthrough(),"rag_results":retriever,"chat_history":RunnablePassthrough()} | self.with_message_history
        self.load_session_data()
    def get_session_history(self,session_id:int):
        if session_id not in self.session_data.keys():
            self.session_data[session_id]=SQLChatMessageHistory(session_id,"sqlite:///files/chat_history.db")
            self.session_data[session_id].add_message(SystemMessage(self.system_prompt))
            self.session_data[session_id].add_message(AIMessage(self.greeting_prompt))
        return self.session_data[session_id]
    def load_session_data(self):
        with sqlite3.connect("files/chat_history.db") as client:
            #创建游标对象
            cursor = client.cursor()
            cursor.execute("select count(*) from sqlite_master where type='table' and name='message_store'")
            if cursor.fetchall()[0][0]==0:
                self.session_data={}
            else:
                cursor.execute("select distinct session_id from message_store")
                session_ids=cursor.fetchall()

                self.session_data={
                    int(session_id[0]):SQLChatMessageHistory(
                        session_id[0],"sqlite:///files/chat_history.db"
                      ) for session_id in session_ids
                }
    def chat(self,input:str,session_id:int):
        config={"configurable":{"session_id":session_id}}
        response = self.chain.invoke(input, config)
        return response.content
    def stream(self,input:str,session_id:int):
        config={"configurable":{"session_id":session_id}}
        response = self.chain.stream(input, config)
        return response
