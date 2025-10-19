# backend/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import text
from backend.database import SessionLocal
from backend.schema import QueryRequest
from backend.llm_chain import chain, extract_sql
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


import os

# Load .env file
load_dotenv()

# Access variables
api_key = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
os.environ["LANGCHAIN_API_KEY"] = api_key
os.environ["LANGCHAIN_PROJECT_NAME"] = os.getenv("LANGCHAIN_PROJECT_NAME", "Default_Project")

app = FastAPI(title="AI Query-to-SQL API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific Lovable URL
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/query")
def run_query(request: QueryRequest):
    question = request.question
    db = SessionLocal()
    try:
        # Step 1: Convert natural language → SQL
        llm_response = chain.run(question)
        sql_query = extract_sql(llm_response)
        print(f"Generated SQL:\n{sql_query}")

        # Step 2: Allow only SELECT queries
        if not sql_query.strip().upper().startswith("SELECT"):
            raise HTTPException(status_code=400, detail="Only SELECT queries are allowed.")

        # Step 3: Make string comparisons case-insensitive for SQLite
        # Replace = comparisons on string columns with COLLATE NOCASE
        sql_query_ci = sql_query
        string_columns = ["department", "name"]  # add any other text columns in your DB
        for col in string_columns:
            sql_query_ci = sql_query_ci.replace(
                f"{col} =", f"{col} COLLATE NOCASE ="
            )

        # Step 4: Execute SQL
        result = db.execute(text(sql_query_ci))
        rows = result.fetchall()
        columns = result.keys()

        # Step 5: Convert to list of dicts
        results = [dict(zip(columns, row)) for row in rows]

        # Step 6: Friendly message if no results
        if not results:
            return {
                "query": sql_query,
                "results": [],
                "message": "No matching data found for your query in the database."
            }

        return {"query": sql_query, "results": results}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        db.close()

