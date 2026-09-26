import asyncio
import logging
import re
from typing import List, Tuple, Optional
from duckduckgo_search import DDGS

logger = logging.getLogger("nova_agent.tools")

class Tools:
    """Implementation of tools for NovaAgent."""

    @staticmethod
    async def calculator(expression: str) -> str:
        """
        Evaluates a mathematical expression.
        Supports basic arithmetic: +, -, *, /, **, ().
        """
        logger.info(f"Executing Calculator: {expression}")
        # Clean expression to allow only safe characters
        clean_expr = re.sub(r"[^0-9+\-*/().\s]", "", expression)
        try:
            # Using eval for simplicity in this local agent context,
            # but restricted to math characters for safety.
            result = eval(clean_expr, {"__builtins__": {}})
            return str(result)
        except Exception as e:
            return f"Error calculating: {str(e)}"

    @staticmethod
    async def web_search(query: str) -> str:
        """
        Performs a DuckDuckGo instant-answer web search.
        """
        logger.info(f"Executing Web Search: {query}")
        try:
            with DDGS() as ddgs:
                # Use the 'answers' feature for instant results
                results = ddgs.answers(query, max_results=1)
                if results:
                    return results[0]['Answer']

                # Fallback to general search if no instant answer
                search_results = list(ddgs.text(query, max_results=3))
                if search_results:
                    return "\n".join([f"{r['title']}: {r['body']}" for r in search_results])

                return "No results found."
        except Exception as e:
            return f"Search error: {str(e)}"

# Map for the planner to easily call tools
TOOL_MAP = {
    "calculator": Tools.calculator,
    "web_search": Tools.web_search
}
