# backend/llm_chain.py
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import Ollama

# LLM setup
llm = Ollama(model="llama3")  # Use your locally installed model

# Prompt template
prompt = PromptTemplate(
    input_variables=["question"],
    template=(
        "You are an expert SQL generator for SQLite. "
        "Generate a valid SQL query using the exact table and column names in lowercase.\n"
        "Use only SELECT statements. Do not add explanations.\n\n"
        "Database schema: \n"
        "- Table employees (id, name, department, salary)\n"
        "- You can add more tables as needed\n\n"
        "Question: {question}\nSQL Query:"
    )
)

chain = LLMChain(llm=llm, prompt=prompt)

def extract_sql(llm_response: str) -> str:
    """
    Extract exactly one SQL statement from LLM response.
    """
    # Try to find ```sql ... ``` blocks
    match = re.search(r"```sql(.*?)```", llm_response, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        # fallback: take only the first line that looks like a SQL statement
        sql = llm_response.strip().split(";")[0] + ";"

    # Remove any extra text after the first semicolon
    sql = sql.split(";")[0].strip() + ";"
    return sql
