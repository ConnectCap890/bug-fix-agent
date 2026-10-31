import os
import subprocess
import json
from pathlib import Path
import time
import uuid
import requests 

# Path safety

TASKS_DIR = Path("tasks").resolve()

def safe_path(user_path: str) -> Path:
    """
    Ensures that the provided user_path is within the TASKS_DIR.
    """
    resolved = (TASKS_DIR / user_path).resolve()
    if not resolved.is_relative_to(TASKS_DIR):
        raise ValueError(f"Path escape blocked: {user_path!r}")
    return resolved

#tool functions

def list_dir(path: str = ".") -> str:

    """list the contents of a directory"""
    target = safe_path(path)
    entries = sorted(target.iterdir())
    return "\n".join(e.name for e in entries)

def read_file(path: str) -> str:
    """read the contents of a file"""

    target = safe_path(path)
    return target.read_text(encoding="utf-8")

def write_file(path: str, content: str) -> str:

    target = safe_path(path)
    target.write_text(content, encoding ="utf-8")
    return f"File {path} written successfully."

def run_tests() -> str:

    """
    run pytest on the tasks directory and return output
    """
    
    result = subprocess.run(
        ["python", "-m","pytest",str(TASKS_DIR),"--tb=short","-q"],
        capture_output=True,
        text= True
    )

    return result.stdout + result.stderr

#tool schemas
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List all files in the tasks directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path inside tasks/ to list. Default is '.' for the tasks folder itself"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file inside the tasks folder",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file, e.g. 't01.py' or 'test_t01.py'"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write new content to a file inside the tasks folder, overwriting it completely",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file, e.g. 't01.py'"
                    },
                    "content": {
                        "type": "string",
                        "description": "The new file content to write"
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_tests",
            "description": "Run pytest on all tasks and return the output. Use this to check which bugs are fixed and which are not",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

#Tool dispatcher

TOOL_MAP = {
    "list_dir": list_dir,
    "read_file": read_file,
    "write_file": write_file,
    "run_tests": run_tests,
}

def tool_dispatcher(name: str, args: dict) -> tuple[ str, bool]:
    """
    Dispatches the tool call to the appropriate funtion 
    """
    if name not in TOOL_MAP:
        return f"Unknown Tool:{name}", False
    try:
        result = TOOL_MAP[name](**args)
        return str(result), True
    except Exception as e:
        return f"Error: {e}", False


#Agent Loop

MAX_STEPS = 20
MAX_SECONDS = 300

def run_agent(task_id:str, model: str = "llama3.2:3b"):

    run_id = uuid.uuid4().hex[:8]
    run_dir = Path("runs")/ run_id
    run_dir.mkdir(parents=True,exist_ok=True)
    trace_path = run_dir/ "trace.jsonl"

    print(f"\n{'='*50}")
    print(f"RUN ID: {run_id}")
    print (f"Task:{task_id}")
    print (f"Model:{model}")
    print(f"{'='*50}\n")

    messages = [
             { "role": "system",
               "content": (
                             "You are a Python bug-fixing agent. "
                             "You have tools to list files, read files, write files, and run tests. "
                             "Your job is to find and fix the bug in the given task file so all tests pass. "
                             "Always run the tests first to see what is failing, then read the buggy file, "
                             "fix it with write_file, then run tests again to confirm. "
                             "Only fix files inside the tasks folder."
                         ) 
             },
             {
                 "role": "user",
                 "content": f"Fix the bug in {task_id}.py so that test_{task_id}.py passes."
             }
        ]
    step = 0
    start_time = time.time()
    stop_reason = "max_steps"


    #main loop

    while step < MAX_STEPS:

        # check time limit
        if time.time() - start_time > MAX_SECONDS:
            stop_reason = "timeout"
            break

        step += 1
        print(f"Step {step}")

        # call the model
        t0 = time.time()
        try:
            resp = requests.post(
                "http://localhost:11434/v1/chat/completions",
                json={
                    "model":       model,
                    "messages":    messages,
                    "tools":       TOOLS,
                    "tool_choice": "auto",
                },
                timeout=300,
            )
            resp.raise_for_status()
        except Exception as e:
            print(f"  API error: {e}")
            stop_reason = "api_error"
            break

        ms     = int((time.time() - t0) * 1000)
        data   = resp.json()
        choice = data["choices"][0]
        msg    = choice["message"]

        # add assistant response to message history
        messages.append(msg)

        # check if model is done
        if choice["finish_reason"] == "stop":
            print(f"  Model finished: {msg.get('content', '')}")
            stop_reason = "done"
            break

        # get tool calls from response
        tool_calls = msg.get("tool_calls", [])
        if not tool_calls:
            print("  No tool calls returned, stopping.")
            stop_reason = "no_tool_calls"
            break

        # process each tool call
        for tc in tool_calls:
            fn        = tc.get("function", {})
            tool_name = fn.get("name", "")
            raw_args  = fn.get("arguments", "{}")

        
            valid_call = True
            try:
                args = json.loads(raw_args)
                if not isinstance(args, dict):
                    raise ValueError("args not a dict")
            except Exception:
                args       = {}
                valid_call = False

            # check tool name is valid
            if tool_name not in TOOL_MAP:
                valid_call = False

            # check required args are present
            for schema in TOOLS:
                if schema["function"]["name"] == tool_name:
                    required = schema["function"]["parameters"].get("required", [])
                    if any(r not in args for r in required):
                        valid_call = False
                    break

            # run the tool
            t1 = time.time()
            result, ok = tool_dispatcher(tool_name, args)
            tool_ms = int((time.time() - t1) * 1000)

            print(f"  Tool       : {tool_name}")
            print(f"  Args       : {args}")
            print(f"  Ok         : {ok}")
            print(f"  Valid call : {valid_call}")
            print(f"  Preview    : {result[:80]}\n")

            # log to trace.jsonl
            log_entry = {
                "step":           step,
                "task":           task_id,
                "model":          model,
                "tool":           tool_name,
                "args":           args,
                "ok":             ok,
                "valid_call":     valid_call,
                "result_preview": result[:120],
                "ms":             tool_ms,
                "ts":             time.time(),
            }
            with open(trace_path, "a") as f:
                f.write(json.dumps(log_entry) + "\n")

            # send tool result back to model
            messages.append({
                "role":         "tool",
                "tool_call_id": tc.get("id", ""),
                "content":      result,
            })

    # ── run complete ──────────────────────────────────────────────────────────
    elapsed = int(time.time() - start_time)
    print(f"\n{'='*50}")
    print(f"Stopped : {stop_reason}")
    print(f"Steps   : {step}")
    print(f"Time    : {elapsed}s")
    print(f"Trace   : {trace_path}")
    print(f"{'='*50}\n")

    # log stop reason
    with open(trace_path, "a") as f:
        f.write(json.dumps({
            "event":       "run_complete",
            "task":        task_id,
            "model":       model,
            "stop_reason": stop_reason,
            "steps":       step,
            "elapsed_s":   elapsed,
        }) + "\n")


# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tasks = [f"t{str(i).zfill(2)}" for i in range(1, 11)]
    for task_id in tasks:
        run_agent(task_id, model="llama3.2:3b")
         
