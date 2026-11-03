# Bug-Fix Agent

A plain-Python agent that fixes bugs in Python files using a local LLM (Ollama).
No frameworks — just a raw loop that calls tools, reads results, and tries again.

## What it does

1. Sends a buggy Python file to a local model
2. Model calls tools to read the file, run tests, and write a fix
3. Agent runs the tools and sends results back to the model
4. Repeats until the tests pass or the limit is hit (20 steps / 5 minutes)

## Requirements

- Python 3.10+
- [Ollama v0.3.14](https://github.com/ollama/ollama/releases/tag/v0.3.14) — use this version, newer versions crash on some hardware
- A model with tool support, e.g. `llama3.2:3b`

## Setup

```bash
# 1. Pull a model
ollama pull llama3.2:3b

# 2. Install dependencies
pip install requests pytest

# 3. Create the buggy task files
python setup.py

# 4. Run the agent
python agent.py
```

## Project Structure

```
bug-fix-agent/
├── setup.py       ← creates 10 buggy Python files and their tests in tasks/
├── agent.py       ← the agent loop, tools, and logging
├── tasks/         ← buggy files + tests (created by setup.py)
└── runs/          ← one folder per run, each has a trace.jsonl log
```

## Logs

Every tool call is saved as one JSON line in `runs/<run-id>/trace.jsonl`:

```json
{"step": 2, "task": "t01", "model": "llama3.2:3b", "tool": "read_file", "args": {"path": "t01.py"}, "ok": true, "valid_call": true, "result_preview": "def is_even(n): ...", "ms": 812, "ts": 1793300000.1}
```
