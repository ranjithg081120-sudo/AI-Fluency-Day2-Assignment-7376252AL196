"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator
from config import COMPONENT_COSTS

def get_item_cost(item: str) -> str:
    """Look up the cost of one component (ARDUINO, SENSOR, or GSM)."""
    cost = COMPONENT_COSTS.get(item.strip().upper())
    return str(cost) if cost is not None else f"Unknown item: {item}"

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg}

def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")

def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (1450 + 980) * 0.9."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"

TOOL_FUNCTIONS = {"get_item_cost": get_item_cost, "calculator": calculator}

TOOLS = [
    {"type": "function", "function": {
        "name": "get_item_cost",
        "description": "Get the cost in rupees for a single component, for example ARDUINO.",
        "parameters": {"type": "object",
                       "properties": {"item": {"type": "string"}},
                       "required": ["item"]}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                       "properties": {"expression": {"type": "string"}},
                       "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("get_item_cost('sensor') ->", get_item_cost("sensor"))
    print("calculator('(1450 + 980) * 0.9') ->", calculator("(1450 + 980) * 0.9"))