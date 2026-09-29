import sys, json
from client import TodayAIProactiveAgendaSynthesizer

def handle_mcp():
    today_ai = TodayAIProactiveAgendaSynthesizer()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(today_ai.run_today_ai_benchmark(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            
            if method == "initialize":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {
                    "protocolVersion": "2024-11-05",
                    "serverInfo": {"name": "genpark-today-ai-proactive-daily-agenda-synthesizer-skill", "version": "1.0.0"},
                    "capabilities": {"tools": {}}
                }}
            elif method == "tools/list":
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [
                    {"name": "ingest_daily_signals", "description": "Ingest calendar events and tasks.", "inputSchema": {"type": "object", "properties": {"calendar_events": {"type": "array"}, "pending_tasks": {"type": "array"}}}},
                    {"name": "synthesize_proactive_schedule", "description": "Synthesize circadian-optimized schedule.", "inputSchema": {"type": "object", "properties": {"target_date": {"type": "string"}}}},
                    {"name": "generate_morning_briefing", "description": "Generate executive briefing brief.", "inputSchema": {"type": "object", "properties": {"agenda": {"type": "object"}}}},
                    {"name": "run_today_ai_benchmark", "description": "Run Today AI benchmark.", "inputSchema": {"type": "object"}}
                ]}}
            elif method == "tools/call":
                tname = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if tname == "ingest_daily_signals":
                    res = today_ai.ingest_daily_signals(args.get("calendar_events"), args.get("pending_tasks"))
                elif tname == "synthesize_proactive_schedule":
                    res = today_ai.synthesize_proactive_schedule(args.get("target_date", "today"))
                elif tname == "generate_morning_briefing":
                    res = today_ai.generate_morning_briefing(args.get("agenda", {}))
                else:
                    res = today_ai.run_today_ai_benchmark()
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    handle_mcp()
