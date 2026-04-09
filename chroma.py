from langchain_community.document_loaders.pdf import PDFMinerLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_zhipu import ZhipuAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
load_dotenv()
class MyChroma(Chroma):
    embedding=ZhipuAIEmbeddings(api_key=os.getenv("ZHIPU_API_KEY"),
                                model="embedding-2")

    def add_file(self,filename):
        document=PDFMinerLoader(filename).load()
        splits=RecursiveCharacterTextSplitter(chunk_size=200,chunk_overlap=40).split_documents(document)
        self.add_documents(splits)
    @classmethod
    def from_folder(cls,persist_directory,collection_name,folder_path=None):
        self=cls(collection_name,cls.embedding,persist_directory)

        if folder_path:
            files=[os.path.join(folder_path,f) for f in os.listdir(folder_path) if f.endswith(".pdf")]
            for file in files:
                self.add_file(file)
        return self

