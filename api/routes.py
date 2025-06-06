from fastapi import APIRouter
from schemas import QueryRequest
import globals
import psycopg2
from psycopg2.extras import RealDictCursor

router = APIRouter()

def get_db_connection():
    return psycopg2.connect(
        dbname="chatbotdb",
        user="postgres",
        password="postgres",
        host="db",
        port="5432"
    )

@router.post("/ask/")
async def ask_question(request: QueryRequest):
     
    if globals.qa_chain is None:
        return {"error": "QA chain is not initialized yet."}
    
    # Save user message
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_sessions (role, message) VALUES (%s, %s)",
        ("user", request.query)
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
        "INSERT INTO chat_sessions (role, message) VALUES (%s, %s)",
        ("assistant", full_answer)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {"answer": full_answer}

@router.get("/session/")
async def get_session():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT role, message, created_at FROM chat_sessions ORDER BY created_at ASC LIMIT 10"
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
