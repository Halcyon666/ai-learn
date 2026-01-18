# 文件名: client.py
import asyncio
import sys
import operator
from typing import Annotated, TypedDict, List

# MCP SDK
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# LangChain / LangGraph
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, END

# --- 1. 定义状态 ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# --- 2. 转换器：把 MCP 工具变成 LangChain 工具 ---
def mcp_to_langchain(mcp_tool, session):
    async def _tool_func(**kwargs):
        # 调用 MCP Server
        result = await session.call_tool(mcp_tool.name, arguments=kwargs)
        # 提取结果文本
        if result.content and result.content[0].type == "text":
            return result.content[0].text
        return str(result)

    return StructuredTool.from_function(
        func=None,
        coroutine=_tool_func, # LangChain 支持异步工具
        name=mcp_tool.name,
        description=mcp_tool.description
    )

# --- 3. 主程序 ---
async def main():
    # 配置服务器启动参数
    server_params = StdioServerParameters(
        command=sys.executable, 
        args=["D:/project/PycharmProjects/fastApiProject/mcp-server.py"], 
        env=None
    )

    print("🔌 Client: 正在连接 MCP Server...")

    # 建立连接
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化
            await session.initialize()
            
            # 获取工具
            tools_data = await session.list_tools()
            mcp_tools = tools_data.tools
            print(f"🛠️  Client: 发现工具 -> {[t.name for t in mcp_tools]}")

            # 转换工具给 LangChain
            lc_tools = [mcp_to_langchain(t, session) for t in mcp_tools]

            # 初始化 LLM (确保你的 Ollama 已经 pull 了 llama3.1 或 qwen2.5)
            llm = ChatOllama(model="llama3.1", temperature=0)
            llm_with_tools = llm.bind_tools(lc_tools)

            # --- 构建 LangGraph ---

            async def call_model(state: AgentState):
                # 调用 LLM
                response = await llm_with_tools.ainvoke(state["messages"])
                return {"messages": [response]}

            async def call_tools(state: AgentState):
                last_message = state["messages"][-1]
                results = []
                for call in last_message.tool_calls:
                    print(f"🤖 Agent: 决定调用工具 '{call['name']}' 参数: {call['args']}")
                    
                    # 查找并执行工具
                    tool = next((t for t in lc_tools if t.name == call['name']), None)
                    if tool:
                        output = await tool.coroutine(**call['args'])
                        print(f"✅ Agent: 工具返回结果 -> {output}")
                        
                        results.append(ToolMessage(
                            content=output,
                            tool_call_id=call["id"],
                            name=call["name"]
                        ))
                return {"messages": results}

            # 定义图结构
            workflow = StateGraph(AgentState)
            workflow.add_node("llm", call_model)
            workflow.add_node("tools", call_tools)
            workflow.set_entry_point("llm")

            # 条件边：有 tool_calls 就去 tools，否则结束
            workflow.add_conditional_edges(
                "llm",
                lambda s: "tools" if s["messages"][-1].tool_calls else END
            )
            workflow.add_edge("tools", "llm")

            agent = workflow.compile()

            # --- 运行测试 ---
            query = "请计算 100 加上 55 等于多少？"
            print(f"\n👤 用户: {query}")
            print("-" * 50)

            inputs = {"messages": [HumanMessage(content=query)]}
            
            # 运行图
            async for chunk in agent.astream(inputs, stream_mode="values"):
                # 只打印每一步最后一条消息的内容
                msg = chunk["messages"][-1]
                # print(f"[{msg.type}]: {msg.content}") 

            # 打印最终回复
            print("-" * 50)
            print(f"💡 最终答案: {chunk['messages'][-1].content}")

if __name__ == "__main__":
    asyncio.run(main())
    
"""
🔌 Client: 正在连接 MCP Server...
🛠️  Client: 发现工具 -> ['add_numbers']

👤 用户: 请计算 100 加上 55 等于多少？
--------------------------------------------------
🤖 Agent: 决定调用工具 'add_numbers' 参数: {'a': 100, 'b': 55}
✅ Agent: 工具返回结果 -> {
  "result": 155
}
--------------------------------------------------
💡 最终答案: 100 加上 55 等于 155。
    
"""