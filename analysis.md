# Analysis: Direct Prompting vs Chain-of-Thought vs ReAct

## Scenario
A PBL project team's private component budget — Arduino Uno kit (Rs. 1,450), Ultrasonic sensor (Rs. 320), GSM module (Rs. 980) — data no public LLM has seen, combined with general reasoning questions about scheduling and budget splitting.

## 1. Explanation of each approach

**Direct prompting** answers immediately from the model's own knowledge, with no visible reasoning and no tool access. On our scheduling and budget-split questions, it happened to answer correctly, since these were simple enough to compute in one step. On the component-cost question, however, it could only return a formula, and on the sensor-cost question it fabricated a plausible-sounding but completely wrong answer, since it has no access to our actual data.

**Chain-of-Thought** makes the model reason step by step before answering, which improves multi-step reasoning but cannot supply facts the model does not already know. It correctly worked through the scheduling and budget-split questions with clear, numbered steps, catching a subtlety (splitting 15 days into 3 equal parts) that direct prompting stated without explanation. However, on the component-cost question it could only produce an algebraic expression, and on the sensor-cost question it invented a "median market price" from generic online listings ($3.50), still with no connection to the real answer (Rs. 320). Better reasoning did not fix the missing data.

**ReAct** cycles through Thought, Action and Observation — it reasons about what it needs, calls a tool to get it, observes the result, and repeats until it can give a final answer. On the reasoning-only questions, it produced the same correct answers as CoT, this time without needing a tool. On the two data questions, it correctly called get_item_cost to fetch real prices (Rs. 1,450 for Arduino, Rs. 980 for GSM, Rs. 320 for sensor) and calculator to apply the discount, arriving at the correct final answers (Rs. 2,187 and Rs. 320) that neither direct prompting nor CoT could reach.

## 2. Comparison table

| Basis | Direct prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | None shown | Step-by-step, visible | Step-by-step, visible, plus tool results |
| Tool usage | None | None | Yes (get_item_cost, calculator) |
| Reliability on multi-step questions | Inconsistent — no way to verify | Higher, but still fails when facts are missing | Highest — grounded by real data |
| Transparency | None (black box) | Full — every step is shown | Full — steps and tool calls are shown |
| Speed / cost | Fastest, one call | Slower, longer replies | Slowest — multiple calls (reasoning + tool calls) |
| Consistency across repeated runs | Not tested here | Mostly consistent (3 of 5 runs matched exactly, 2 had wording differences but the same number) | Deterministic at temperature 0 |

## 3. Self-consistency observation
Running the budget-split question (Q2) 5 times at temperature 0.8 produced Rs. 750 in all 5 runs, with only minor wording differences ("750" vs "Rs. 750 per category"), giving a majority answer of 3 of 5 exact-text matches, all numerically correct. This shows the model was highly consistent on this particular question, likely because the calculation was simple enough that reasoning errors were unlikely. At temperature 0, all 5 runs would be expected to produce nearly identical text, since the model's output becomes deterministic and voting would add little value beyond confirming the single answer.

## 4. Suitability analysis
For this scenario, the **ReAct agent** is most suitable. It matched CoT's reasoning ability on the scheduling and budget questions while being the only approach to correctly answer the component-cost questions, which depend on private data. The self-consistency test shows that even where CoT reasoning is reliable, it remains fundamentally limited whenever a question needs real, private information — a limitation ReAct removes by calling tools rather than guessing.

## 5. Conclusion
Direct prompting is appropriate for simple, low-stakes questions where speed matters more than transparency or accuracy on unfamiliar facts. Chain-of-Thought is appropriate when a question requires careful multi-step reasoning but all necessary information is already within the model's general knowledge — it improves reliability without needing tools. A ReAct agent is necessary whenever a task requires both careful reasoning and access to real, private, or up-to-date information that the model cannot know on its own; without tools, even excellent reasoning will confidently produce wrong answers, as shown clearly by the hallucinated sensor price under Chain-of-Thought prompting.