import asyncio
import logging
from typing import List, Tuple
from tools import TOOL_MAP

logger = logging.getLogger("nova_agent.planner")

class Planner:
    """
    Handles multi-step request planning and execution.
    Intercepts complex queries, generates a plan, executes tools,
    and synthesizes the final response.
    """

    def __init__(self, llm):
        self.llm = llm

    async def generate_plan(self, user_input: str) -> List[Tuple[str, str]]:
        """
        Prompts the LLM to create a numbered plan of tool calls.
        Returns a list of (tool_name, query) tuples.
        """
        prompt = (
            f"The user has asked: '{user_input}'. "
            "If this requires multiple steps or external data, create a short numbered plan. "
            "Use exactly this format for each step:\n"
            "1. [tool_name] query\n"
            "Available tools: 'calculator', 'web_search'.\n"
            "If no tools are needed, respond with 'NO_PLAN'."
        )

        response = await self.llm.chat(prompt)
        text = response.content

        if "NO_PLAN" in text or not text.strip():
            return []

        # Parse numbered list: "1. [calculator] 5 * 5"
        plan = []
        lines = text.splitlines()
        for line in lines:
            match = re.search(r"(\d+)\.\s*\[(\w+)\]\s*(.*)", line)
            if match:
                tool_name, query = match.group(2), match.group(3)
                if tool_name in TOOL_MAP:
                    plan.append((tool_name, query))

        return plan

    async def execute_plan(self, user_input: str) -> str:
        """
        Main loop: Plan -> Execute -> Synthesize.
        """
        # 1. Generate Plan
        plan = await self.generate_plan(user_input)

        if not plan:
            # Simple query, just let LLM answer
            return await self.llm.chat(user_input).content

        print(f"\n--- Generated Plan ---\n{user_input}\n")
        for i, (tool, query) in enumerate(plan, 1):
            print(f"Step {i}: {tool}({query})")
        print("---------------------\n")

        context = [f"User: {user_input}"]

        # 2. Execute Steps
        for i, (tool_name, query) in enumerate(plan, 1):
            tool_fn = TOOL_MAP[tool_name]
            result = await tool_fn(query)
            print(f"Step {i} Result: {result}")
            context.append(f"Tool {tool_name} result: {result}")

        # 3. Final Synthesis
        final_prompt = (
            "Based on the following interaction and tool results, provide a concise, "
            "natural-sounding spoken answer for the user.\n\n"
            f"Context:\n{' '.join(context)}"
        )

        final_response = await self.llm.chat(final_prompt)
        return final_response.content

# Need import re for the regex in generate_plan
import re
