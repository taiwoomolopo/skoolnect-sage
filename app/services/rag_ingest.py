import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

DATA_PATH = "skoolnect_data"

def ingest_documents():
    documents = []

    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith(".md") or file.endswith(".txt"):
                loader = TextLoader(os.path.join(root, file))
                documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embeddings, persist_directory="./chroma_db")
    

if __name__ == "__main__":
    ingest_documents()