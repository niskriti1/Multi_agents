import os
from dotenv import load_dotenv
from agno.tools import tool
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.team import Team


load_dotenv()

os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

@tool
def add(a:int,b:int) -> int:
    """Addition of numbers."""
    return a+b
    
@tool
def subtract(a:int,b:int) -> int:
    """Subtraction of numbers."""
    return a-b

@tool
def product(a:int,b:int) -> int:
    """Multiplication of numbers."""
    return a*b
@tool
def division(a:int,b:int) -> int:
    """Division of numbers."""
    return a/b

calculator_agent = Agent(
	name = "Calculator Agent",
	role="Performs arithmetic operations",
	model=Gemini(id="gemini-2.0-flash"),
	tools=[add,subtract,product,division],
	instructions="You are a calculation expert. Use the tools given to perform calculations. If unsure or need more clarity ask user to clarify or for more information.",
	show_tool_calls=True,
	markdown=True,
)  
  

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[DuckDuckGoTools()],
    instructions="You are a web search expert. Use the tools given to search for user's queries. If unsure or need more clarity ask user to clarify or for more information.Always include sources",
    show_tool_calls=True,
    markdown=True,
)


finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Gemini(id="gemini-2.0-flash"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,company_news=True)],
    instructions="You are a finance expert. Use the tools given to perform finance related tasks. If unsure or need more clarity ask user to clarify or for more information. Use tables to display data",
    show_tool_calls=True,
    markdown=True
)



agent_team = Team(
      mode="coordinate",
      members=[web_agent, finance_agent, calculator_agent],
      model=Gemini(id="gemini-2.0-flash"),
      success_criteria="Proper result for the questions with related tools.",
      instructions=[
      "Always include sources when relevant (e.g., for facts or search results).",
      "Use the **calculator agent** for any arithmetic, such as addition, subtraction, multiplication, or percentage calculations.",
      "Use the **finance agent** to answer queries related to stock prices, company valuations, financial history, or market data.",
      "Use the **web agent** to search the internet for current events, news, or information not available in the system's internal knowledge.",
      "If the user greets (e.g., 'hi', 'hello', 'hey', 'good morning'), respond normally by greeting and ask if you could assist them and **do not use any tool**.",
      "Do not fabricate responses. Only use a tool when appropriate and provide accurate, grounded answers."
    ],
      show_tool_calls=True,
      markdown=True,
      add_history_to_messages=True,
      num_history_runs=50
  )

def get_response(user_query):
  result = agent_team.run(user_query)
  return  result.content


