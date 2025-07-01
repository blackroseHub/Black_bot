from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY

def create_vector_store(chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectordb = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
    vectordb.persist()
    return vectordb

def load_vector_store():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
