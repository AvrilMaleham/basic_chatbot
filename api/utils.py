from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def load_vectorstore(load_path="vectorstore"):
    """Load FAISS vectorstore"""
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)

def create_qa_chain(vectorstore):
    """Return RetrievalQA chain"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    retriever = vectorstore.as_retriever()
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
