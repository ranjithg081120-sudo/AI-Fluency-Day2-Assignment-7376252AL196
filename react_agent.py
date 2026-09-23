"""ReAct agent: LLM + tools + loop. Reasons, acts, observes, repeats."""
import json
import re
import time
from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS

SYSTEM_PROMPT = (
    "You are a project budget assistant. Never guess a component cost: always use "
    "get_item_cost. Use calculator for any arithmetic. Available items: ARDUINO, "
    "SENSOR, GSM. If no tool is needed, reason it out and answer directly."
)

def run_tool_call(name, arguments, verbose, step):
    clean_name = name.split("<|")[0].strip()
    function = TOOL_FUNCTIONS.get(clean_name)
    result = function(**arguments) if function else f"Unknown tool: {clean_name}"
    if verbose:
        print(f"   step {step}: {clean_name}({arguments}) -> {result}")
    return clean_name, result

def call_model(messages, retries=6):
    """Call the model, retrying if it returns a malformed/unparsable reply."""
    last_error = None
    for attempt in range(retries):
        try:
            return client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS, temperature=0)
        except Exception as e:
            last_error = e
            text = str(e)
            match = re.search(r"'failed_generation':\s*'(\{.*\})'\}\}", text)
            if match:
                return ("RECOVER", match.group(1))
            time.sleep(2)
    raise last_error

def agent(question, max_steps=8, verbose=True):
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    for step in range(1, max_steps + 1):
        try:
            result = call_model(messages)
        except Exception as e:
            return f"Agent error (could not recover after retries): {e}"

        if isinstance(result, tuple) and result[0] == "RECOVER":
            try:
                call = json.loads(result[1])
            except Exception:
                return f"Agent error (could not parse recovery): {result[1]}"
            name, tool_result = run_tool_call(call["name"], call.get("arguments", {}), verbose, step)
            messages.append({"role": "assistant", "content": "",
                              "tool_calls": [{"id": "recovered_call", "type": "function",
                                              "function": {"name": name,
                                                           "arguments": json.dumps(call.get("arguments", {}))}}]})
            messages.append({"role": "tool", "tool_call_id": "recovered_call", "content": tool_result})
            continue

        message = result.choices[0].message
        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant", "content": message.content or "",
            "tool_calls": [{"id": call.id, "type": "function",
                            "function": {"name": call.function.name,
                                         "arguments": call.function.arguments}}
                           for call in message.tool_calls]})
        for call in message.tool_calls:
            arguments = json.loads(call.function.arguments or "{}")
            _, tool_result = run_tool_call(call.function.name, arguments, verbose, step)
            messages.append({"role": "tool", "tool_call_id": call.id, "content": tool_result})
    return "Stopped: maximum steps reached without a final answer."

if __name__ == "__main__":
    banner("REACT AGENT")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", agent(question))
        print("-" * 70)