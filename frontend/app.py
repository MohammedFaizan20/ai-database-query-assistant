import streamlit as st
import requests
import pandas as pd

BACKEND_URL = " https://unspiriting-scarlett-cyclopaedically.ngrok-free.dev/query"

st.set_page_config(page_title="AI Database Query Assistant", layout="wide")


st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #0D0D0D;
    color: #E0E0E0;
    font-family: 'Segoe UI', sans-serif;
}

/* Header */
h1 {
    color: #9B59B6;
    text-align: center;
    text-shadow: 0 0 10px #9B59B6;
}
p {
    color: #AAAAAA;
    text-align: center;
}

/* Glassy cards */
.stCard, .stExpander {
    background: rgba(30, 30, 30, 0.8);
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    padding: 15px;
    margin-bottom: 15px;
}

/* Table styles */
.dataframe tbody tr:hover {
    background-color: rgba(155, 89, 182, 0.2) !important;
}
.dataframe thead {
    background-color: rgba(50, 50, 50, 0.9);
    color: #FFFFFF;
}

/* Buttons */
.stButton>button {
    background-color: #9B59B6;
    color: #FFFFFF;
    border-radius: 8px;
    font-weight: bold;
    padding: 0.5em 1em;
    box-shadow: 0 0 10px rgba(155, 89, 182, 0.7);
}
.stButton>button:hover {
    background-color: #7D3C98;
    box-shadow: 0 0 15px rgba(155, 89, 182, 0.9);
}

/* SQL code block */
.css-1v3fvcr pre {
    background-color: #1E1E1E !important;
    border-left: 4px solid #9B59B6;
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
}
</style>
""", unsafe_allow_html=True)

#Header
st.markdown("<h1>AI Database Query Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p>Transform natural language into SQL queries instantly</p>", unsafe_allow_html=True)

#Sample data
with st.expander("Sample Data in the Database (click to view)"):
    sample_data = pd.DataFrame([
        {"Name": "Alice", "Department": "HR", "Salary": 60000},
        {"Name": "Bob", "Department": "Engineering", "Salary": 45000},
        {"Name": "Charlie", "Department": "Sales", "Salary": 75000},
    ])
    sample_data.index = sample_data.index + 1
    st.table(sample_data)
    st.markdown("**Example queries:**")
    st.markdown("- Show all employees in HR with salary above 50000")
    st.markdown("- List all employees in Engineering with salary above 40000")
    st.markdown("- Who earns more than 70000?")

#Input box
question = st.text_area(
    "Ask a Question",
    placeholder="e.g., Show all employees in Engineering with salary above 50000"
)

#Run query
if st.button("Run Query"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Fetching results..."):
            try:
                response = requests.post(BACKEND_URL, json={"question": question.strip()})
                data = response.json()

                if "query" in data:
                    st.subheader("Generated SQL")
                    st.code(data["query"], language="sql")

                if data.get("results"):
                    st.subheader("Results")
                    df = pd.DataFrame(data["results"])
                    st.dataframe(df)
                else:
                    st.info(data.get("message", "No matching data found"))

            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
