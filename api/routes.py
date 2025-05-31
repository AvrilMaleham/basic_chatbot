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

    if sources:
     top_source_name = sources[0].metadata.get("source", "Unknown").split('/')[-1]
     citations = f"\n\n**📚 Source:**\n- `{top_source_name}`\n"
    else:
     citations = ""

    return {"answer": answer + citations}
