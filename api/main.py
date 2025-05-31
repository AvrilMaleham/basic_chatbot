from fastapi import FastAPI
from pydantic import BaseModel
from utils import load_vectorstore, create_qa_chain
from contextlib import asynccontextmanager

qa_chain = None 

@asynccontextmanager
async def lifespan(app: FastAPI):
    global qa_chain
    vectorstore = load_vectorstore()
    qa_chain = create_qa_chain(vectorstore)
    yield

app = FastAPI(lifespan=lifespan)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def test():
    return {"hello": "world"}

@app.post("/ask")
async def ask_question(request: QueryRequest):
    global qa_chain
    if qa_chain is None:
        return {"error": "QA chain is not initialized yet."}

    response = qa_chain.invoke({"query": request.query})
    answer = response.get("result", "Sorry, I couldn't find an answer.")
    sources = response.get("source_documents", [])
    
    file_names = {source.metadata.get("source", "Unknown").split('/')[-1] for source in sources}
    
    citations = "\n\n**📚 Source(s):**\n"
    for name in sorted(file_names):
        citations += f"- `{name}`\n"

    return {"answer": answer + citations}
