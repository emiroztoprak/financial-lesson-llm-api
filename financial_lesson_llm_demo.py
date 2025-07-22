import os, json, openai, sys
from datetime import datetime
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

user_profile = {
    "age": 24,
    "location": "Istanbul, Turkey",
    "Occupation": "Software Developer",
    "Language": "English",
    "Goal": "Working as a freelancer"
}

model_name     = "gpt-4o-mini"
temperature    = 0.0

system_msg = """
Your job is to increase the financial literacy of a person who may be living in different contexts such as language, location etc.
Depending on these data, I want you to give a number of financial advices to this person.
Your response must be in JSON format, and must be personalized and region‑specific according to the input.

EXAMPLE:
INPUT:
{"age": 24, "location": "Berlin, Germany", "Occupation": "Pharmacy owner", "Language": "English", "Goal": "to grow his/her business"}

OUTPUT:
{"advices": ["focus on marketing top‑selling products", "reduce stock or discontinue low sellers", "add wellness kits to your offerings"]}
"""



user_msg = f"""
INPUT:
{json.dumps(user_profile, ensure_ascii=False)}

OUTPUT:
"""
messages = [
    {"role": "system", "content": system_msg},
    {"role": "user",   "content": user_msg}
]

resp = openai.chat.completions.create(
    model=model_name,
    messages=messages,
    temperature=temperature
)

answer = resp.choices[0].message.content
print(answer)

try:
    lessons = json.loads(answer)["advices"]
    if isinstance(lessons, str):
        lessons = [lessons]
except Exception:
    lessons = [answer]

def log_output(model_name: str,
               temperature: float,
               messages: list[str],
               user_profile: dict,
               lessons: list[str]) -> None:
    Path("./output_logs").mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    final_data = {
        "modelName": model_name,
        "temperature": temperature,
        "timestamp": timestamp,
        "userProfile": user_profile,
        "messages": messages,
        "lessons": lessons
    }
    filename = f"./output_logs/log_{model_name}_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)
    print(f"Process complete. Conversation saved to {filename}")

log_output(model_name, temperature, [m["content"] for m in messages] + [answer], user_profile, lessons)
