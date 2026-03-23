import json
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_community.llms import Ollama
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub
from src.config import OLLAMA_BASE_URL, LLM_MODEL
from src.tools import web_search, sql_query, read_pdf
from src.models import QueryRequest, QueryResponse

# Get prompt
prompt = hub.pull("hwchase17/react")

# Set up tools
tools = [web_search, sql_query, read_pdf]
tool_executor = ToolExecutor(tools)

# LLM
llm = Ollama(base_url=OLLAMA_BASE_URL, model=LLM_MODEL)

# Create ReAct agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# FastAPI app
from fastapi import FastAPI
app = FastAPI(title="Agentic Assistant")

@app.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest):
    try:
        result = agent_executor.invoke({"input": req.question})
        return QueryResponse(answer=result["output"], steps=result.get("intermediate_steps", []))
    except Exception as e:
        return QueryResponse(answer=f"Error: {e}")