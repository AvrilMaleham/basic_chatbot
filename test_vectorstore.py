from utils import load_vectorstore

def main():
    vectorstore = load_vectorstore()
    
    # Example query
    query = "When was TechCorp founded?"
    
    # Perform similarity search
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"Query: {query}")
    print("Top 3 relevant chunks:")
    for i, doc in enumerate(results, 1):
        print(f"{i}: {doc.page_content}\n---")

if __name__ == "__main__":
    main()
