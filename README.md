**Multi Agent System**
A multi agent system that lets users to chat with the system with: *Web search*, *Calculator* and *Finance* agents. If user asks come question requiring basic calculations, the **Calculator agent** is called. Similarly finance related queries is handled by **Finance agent**, and if both agents couldn't handle any query it is then sent to **Web agent** to search in the web.

**Features**

### ✅ Modular Task Handling
Each agent is specialized for a domain:
- **Calculator Agent**: Performs arithmetic operations.
- **Web Agent**: Simulates internet search responses.
- **Finance Agent**: Fetches real-time and historical stock prices.

### 🧩 Tool-based Execution
Each agent uses tools registered via LangChain’s `@tool` decorator, enabling:
- Easy tool reuse.
- Clear separation between logic and orchestration.

### 🤖 LLM-Powered Orchestration
Uses Gemini's 2.0 flash model to:
- Interpret user input.
- Delegate tasks to the appropriate agent/tool.
- Combine multiple results into one response.

### 🧠 Memory-based System
-Remembers queries in current conversations 
