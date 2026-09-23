"""Shared configuration: chooses the LLM provider and holds the assignment data."""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()

if PROVIDER == "ollama":
    BASE_URL = "http://localhost:11434/v1"
    API_KEY = "ollama"
    MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
elif PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
elif PROVIDER == "huggingface":
    BASE_URL = "https://router.huggingface.co/v1"
    API_KEY = os.getenv("HF_TOKEN")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")
else:
    raise SystemExit(f"Unknown PROVIDER '{PROVIDER}'. Use ollama, groq or huggingface.")

if not API_KEY:
    raise SystemExit(f"No API key found for PROVIDER={PROVIDER}. Check your .env file.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

# Private data: PBL 170 team's component costs, in rupees
COMPONENT_COSTS = {
    "ARDUINO": 1450,
    "SENSOR": 320,
    "GSM": 980,
}

QUESTIONS = [
    # 1. Pure reasoning - scheduling
    "Our team has 5 members and we need to submit the project report in 15 days, "
    "reviewing it twice before submission with equal gaps. On what days (from day 1) "
    "should each review happen?",
    # 2. Pure reasoning - multi-step math
    "We were allotted Rs. 5,000 for the project. If we spend 40% on hardware and the "
    "rest is split equally between 4 remaining expense categories, how much is spent "
    "on each category?",
    # 3. Needs the tool - private data
    "What is our total cost if we buy the Arduino Uno kit and the GSM module, "
    "with a 10% bulk discount from the vendor on that combined total?",
    # 4. Needs the tool - simple lookup
    "What is the cost of the ultrasonic sensor?",
]

def banner(system_name):
    print(f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n")