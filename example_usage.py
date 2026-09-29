from client import TodayAIProactiveAgendaSynthesizer
import json

today_ai = TodayAIProactiveAgendaSynthesizer()
print("=== TODAY AI PROACTIVE DAILY AGENDA BENCHMARK ===")
res = today_ai.run_today_ai_benchmark()
print(json.dumps(res, indent=2))
