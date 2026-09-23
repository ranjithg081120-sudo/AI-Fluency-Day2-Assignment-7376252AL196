# AI Fluency Training — Day 2 Assignment Task

## Overview
This repository compares three approaches to reasoning and acting — **direct prompting**, **Chain-of-Thought (CoT)**, and a **ReAct agent** — on a private-data scenario involving a PBL project team's budget.

## Scenario
A PBL team's private component costs, unknown to any public LLM:

| Component | Cost (Rs.) |
|---|---|
| Arduino Uno kit | 1,450 |
| Ultrasonic sensor | 320 |
| GSM module | 980 |

Combined with general reasoning questions about scheduling and budget splitting that need no private data.

## Files

| File | Description |
|---|---|
| `config.py` | Shared setup — LLM provider, API client, private component data, and the 4 test questions |
| `tools.py` | Defines the tools (`get_item_cost`, `calculator`) the ReAct agent can use |
| `direct_vs_cot.py` | Asks all 4 questions with direct prompting and with Chain-of-Thought prompting |
| `self_consistency.py` | Runs one CoT reasoning question 5 times at temperature 0.8 and takes the majority answer |
| `react_agent.py` | A ReAct agent (LLM + Tools + Loop) that answers all 4 questions, using tools where needed |
| `analysis.md` | Full written comparison, self-consistency observation, and conclusion |
| `screenshots/` | Terminal output screenshots for all 4 scripts |

## Test questions
1. Scheduling — when should two evenly-spaced reviews happen in a 15-day window? (pure reasoning)
2. Budget split — how much per category after a 40% hardware spend? (pure reasoning)
3. Combined cost of Arduino + GSM with a 10% bulk discount (**needs private data**)
4. Cost of the ultrasonic sensor (**needs private data**)

## How to run

1. Create and activate a virtual environment: