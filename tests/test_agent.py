import pytest
from src.agent import agent_executor

def test_agent_basic():
    result = agent_executor.invoke({"input": "What is the capital of France?"})
    assert "Paris" in result["output"]