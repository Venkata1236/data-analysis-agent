# core/agent.py
# Data Analysis Agent using custom tools
# Concepts: @tool decorator, create_react_agent, AgentExecutor

from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from core.custom_tools import get_all_tools
from core.data_loader import get_dataframe_info


REACT_PROMPT = PromptTemplate.from_template("""You are a data analysis assistant.
You have access to these tools:
{tools}

IMPORTANT RULES:
1. Call get_dataset_info FIRST to understand columns
2. Use exact column names WITHOUT quotes
3. Do NOT wrap Action Input in quotes
4. Give Final Answer immediately after getting results

Format:
Question: the input question
Thought: which tool to use?
Action: must be one of [{tool_names}]
Action Input: input without quotes
Observation: result
Thought: I have the answer
Final Answer: clear answer

Question: {input}
Thought:{agent_scratchpad}""")


def create_agent(api_key: str, temperature: float = 0.0, max_iterations: int = 8):
    """
    Creates a data analysis agent with custom tools.

    Args:
        api_key       : OpenAI API key
        temperature   : response creativity (0 = precise)
        max_iterations: max tool calls before stopping

    Returns:
        AgentExecutor ready to analyze data
    """
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=temperature,
        openai_api_key=api_key
    )

    tools = get_all_tools()

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=REACT_PROMPT
    )

    executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)

    return executor


def run_analysis(executor, query: str) -> dict:
    """
    Runs a data analysis query.

    Args:
        executor: AgentExecutor
        query   : analysis question in plain English

    Returns:
        dict with 'answer' and 'steps'
    """
    try:
        result = executor.invoke({"input": query})
        return {
            "answer": result.get("output", "No answer found."),
            "steps": result.get("intermediate_steps", [])
        }
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "steps": []
        }