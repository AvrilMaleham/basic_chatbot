from fastapi import APIRouter
from schemas import QueryRequest
import globals

router = APIRouter()

@router.post("/")
async def ask_question(request: QueryRequest):
    if globals.qa_chain is None:
        return {"error": "QA chain is not initialized yet."}

    response = globals.qa_chain.invoke({"query": request.query})
    answer = response.get("result", "Sorry, I couldn't find an answer.")
    sources = response.get("source_documents", [])

    file_names = {source.metadata.get("source", "Unknown").split('/')[-1] for source in sources}

    citations = "\n\n**📚 Source(s):**\n"
    for name in sorted(file_names):
        citations += f"- `{name}`\n"

    return {"answer": answer + citations}
