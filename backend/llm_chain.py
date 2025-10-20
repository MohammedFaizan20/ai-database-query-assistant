import re
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama

# Setup Ollama LLM
llm = Ollama(model="llama3")

# Define prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are an expert SQL generator for SQLite. "
        "Generate a valid SQL query using the exact table and column names in lowercase.\n"
        "Use only SELECT statements. Do not add explanations.\n\n"
        "Database schema:\n"
        "- Table employees (id, name, department, salary)\n"
        "- You can add more tables as needed\n\n"
        "Question: {question}\nSQL Query:"
    ),
)

# Build the chain (Runnable-style)
chain = prompt | llm  # ✅ replaces LLMChain in LangChain 1.0

# Extract SQL query
def extract_sql(llm_response: str) -> str:
    match = re.search(r"```sql(.*?)```", llm_response, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        sql = llm_response.strip().split(";")[0] + ";"
    return sql.split(";")[0].strip() + ";"
