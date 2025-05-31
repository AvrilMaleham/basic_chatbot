import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import fitz 
from pathlib import Path

load_dotenv()

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def load_documents(directory="documents_pdf"):
    docs = []
    for pdf_file in Path(directory).glob("*.pdf"):
        text = extract_text_from_pdf(str(pdf_file))
        doc = Document(page_content=text, metadata={"source": str(pdf_file)})
        docs.append(doc)
    return docs

def split_documents(documents):
    """Split documents into chunks"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def build_vectorstore(docs, save_path="vectorstore"):
    """Embed and save FAISS vectorstore"""
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(save_path)
    return vectorstore

def load_vectorstore(load_path="vectorstore"):
    """Load FAISS vectorstore"""
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)

def create_qa_chain(vectorstore):
    """Return RetrievalQA chain"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
