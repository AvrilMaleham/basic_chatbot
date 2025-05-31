from utils import load_documents, split_documents, build_vectorstore

print("Loading documents...")
docs = load_documents()

print("Splitting documents...")
chunks = split_documents(docs)

print("Creating vectorstore...")
build_vectorstore(chunks)

print("Vectorstore built and saved to /vectorstore")
