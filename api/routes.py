from fastapi import APIRouter
from schemas import QueryRequest
import globals
import psycopg2

router = APIRouter()

def get_db_connection():
    return psycopg2.connect(
        dbname="chatbotdb",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )

@router.post("/")
async def ask_question(request: QueryRequest):
    session_id = request.session_id or "default"
     
    if globals.qa_chain is None:
        return {"error": "QA chain is not initialized yet."}
    
    # Save user message
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_sessions (session_id, message, role) VALUES (%s, %s, %s)",
        (session_id, request.query, "user")
    )
    conn.commit()

    # Generate assistant response
    response = globals.qa_chain.invoke({"query": request.query})
    answer = response.get("result", "Sorry, I couldn't find an answer.")
    sources = response.get("source_documents", [])

    if sources:
     top_source_name = sources[0].metadata.get("source", "Unknown").split('/')[-1]
     citations = f"\n\n**📚 Source:**\n- `{top_source_name}`\n"
    else:
     citations = ""
     
    full_answer = answer + citations
     
    # Save assistant response
    cur.execute(
        "INSERT INTO chat_sessions (session_id, message, role) VALUES (%s, %s, %s)",
        (session_id, full_answer, "assistant")
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"answer": full_answer}
