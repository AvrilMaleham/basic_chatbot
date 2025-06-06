import fitz  
import boto3
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

AWS_REGION = os.getenv("AWS_REGION")  
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client("s3", region_name=AWS_REGION)

def extract_text_from_pdf_bytes(pdf_bytes, source_name):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return Document(page_content=text, metadata={"source": source_name})

def load_documents(bucket=S3_BUCKET_NAME, prefix=""):
    docs = []
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
    for obj in response.get("Contents", []):
        key = obj["Key"]
        if not key.lower().endswith(".pdf"):
            continue
        s3_object = s3.get_object(Bucket=bucket, Key=key)
        pdf_bytes = s3_object["Body"].read()
        doc = extract_text_from_pdf_bytes(pdf_bytes, source_name=key)
        docs.append(doc)
    return docs

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)

def build_vectorstore(docs, save_path="vectorstore"):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(save_path)
    return vectorstore
