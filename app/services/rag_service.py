from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

def retrieve_context(query):
    docs = db.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])