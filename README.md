**AI Query-to-SQL API**

This project is an AI-powered backend application that converts natural language questions into SQL queries using LangChain and Ollama (LLaMA 3 model), executes them on a SQLite database, and returns structured results through a FastAPI REST API.

**Overview**

This system allows users to interact with databases conversationally — no SQL knowledge required.
For example, a user can ask:

“Show all employees in the Engineering department earning above 50,000.”

The system uses a Large Language Model (LLaMA 3) to translate that question into an executable SQL query, runs it on the database via SQLAlchemy, and returns the data in a structured JSON response.

**Key Features:**

Converts natural language → SQL queries automatically.

Built on FastAPI for high-performance, asynchronous API serving.

Uses LLaMA 3 via Ollama for on-device LLM inference.

Ensures only safe SELECT queries are executed.

Handles case-insensitive string matching.

Uses SQLAlchemy ORM for secure query execution.

Modular structure for easy scalability and maintenance.

**Project Structure:**
backend/
│
├── __init__.py          # Initializes the package
├── __pycache__/         # Compiled Python cache
│
├── data.db              # SQLite database file
├── database.py          # Database connection setup
├── db_setup.py          # Initial database and table setup script
├── llm_chain.py         # LLM (LangChain + Ollama) setup and SQL generation logic
├── main.py              # FastAPI app entry point and endpoint definitions
├── models.py            # SQLAlchemy ORM models
├── schema.py            # Pydantic models for request validation

**Technical Flow**

1. User Query
A user sends a natural language question (e.g., “List all employees from HR department”) to the /query endpoint.

2. LLM Processing (LangChain + Ollama)

The request is passed to the LangChain prompt pipeline.
The PromptTemplate defines how the question should be framed for the LLM.
Ollama (LLaMA 3) generates an SQL query based on the defined database schema.

3. SQL Extraction
The response from the LLM is parsed by extract_sql() using regex to isolate valid SQL statements.

4. Query Validation and Execution

Only SELECT queries are allowed for security reasons.
SQLAlchemy executes the validated query on the SQLite database.
Results are fetched and converted into a list of dictionaries.

5. Response

A structured JSON response is returned containing:
The generated SQL query.
The query results (if found) or a descriptive message if no data matches.

Core Components

1. main.py
Implements:
 - FastAPI app setup.
 - CORS middleware.
 - /query POST endpoint to handle incoming questions.
 - Integration with the LLM chain and database layer.

2. llm_chain.py
   
 - The LangChain PromptTemplate (SQL generation instructions).
 - Ollama (LLaMA 3) as the local model interface.

extract_sql() function to cleanly extract SQL queries from model outputs.

3. database.py

Configures:
 - Database connection using SQLAlchemy.
 - Session management for executing SQL queries.

4. db_setup.py

Initializes:
 - SQLite database tables.
 - Optionally seeds sample employee data.

5. models.py
 - ORM mapping for the employees table (columns: id, name, department, salary).

6. schema.py
 - Pydantic model (QueryRequest) for request validation.

**Tech Stack:**

| Component          | Technology              |
| ------------------ | ----------------------- |
| API Framework      | FastAPI                 |
| Model Interface    | LangChain + Ollama      |
| LLM Used           | LLaMA 3                 |
| Database           | SQLite (SQLAlchemy ORM) |
| Validation         | Pydantic                |
| Environment Config | python-dotenv           |
| Server             | Uvicorn                 |


**Installation and Setup:**

1. Clone the Repository
git clone https://github.com/your-username/ai-query-to-sql.git
cd ai-query-to-sql

2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root:
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_api_key_here
LANGCHAIN_PROJECT_NAME=SQL_AI_Project

5. Set Up Database

Initialize or reset the database:
python backend/db_setup.py

6. Run Ollama
Ensure Ollama and LLaMA 3 are installed:
ollama pull llama3

7. Start FastAPI Server
uvicorn backend.main:app --reload

8. Test the API
Send a POST request:
http://127.0.0.1:8000/query

Example JSON Request:
{
  "question": "Show all employees in the HR department."
}

Example Response:
{
  "query": "SELECT * FROM employees WHERE department = 'HR';",
  "results": [
{"id": 1, "name": "Alice", "department": "HR", "salary": 60000}
]
}

**Requirements:**
fastapi
uvicorn
pydantic
SQLAlchemy
python-dotenv
langchain
langchain-community
ollama
requests
tqdm

Dependency Overview:
| Library                 | Purpose                                        |
| ----------------------- | ---------------------------------------------- |
| **FastAPI**             | Web framework for serving APIs                 |
| **Uvicorn**             | ASGI server to run FastAPI                     |
| **Pydantic**            | Request/response validation                    |
| **SQLAlchemy**          | ORM and database query execution               |
| **python-dotenv**       | Manage environment variables                   |
| **LangChain**           | Framework for LLM prompt management            |
| **langchain-community** | Integrations for community LLMs (e.g., Ollama) |
| **Ollama**              | Local runtime for LLaMA 3 model                |
| **Requests**            | Send and test API requests                     |
| **tqdm**                | Progress bar for iterative tasks (optional)    |


Future Enhancements:

 - Multi-database support (PostgreSQL, MySQL).
 - Dynamic schema introspection for automatic table detection.
 - User authentication and access control.
 - Query optimization and logging.

