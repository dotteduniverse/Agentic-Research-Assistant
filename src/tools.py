import requests
from langchain.tools import tool
from duckduckgo_search import DDGS
import pypdf
import os
import sqlalchemy
from sqlalchemy import text
from src.config import DATABASE_URL

@tool
def web_search(query: str) -> str:
    """Search the web for information. Input should be a search query."""
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=3))
        if not results:
            return "No results found."
        return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])

@tool
def sql_query(query: str) -> str:
    """Run a SQL query against the synthetic database. Input should be a SQL SELECT statement."""
    try:
        engine = sqlalchemy.create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            if not rows:
                return "No results."
            return "\n".join([str(row) for row in rows])
    except Exception as e:
        return f"Error executing query: {e}"

@tool
def read_pdf(file_name: str) -> str:
    """Read text from a PDF file. Input should be the filename (with .pdf) located in the data folder."""
    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        return f"File {file_name} not found in data folder."
    text = ""
    with open(file_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text[:5000]  # limit to 5000 chars