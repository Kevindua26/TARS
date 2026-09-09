#!/usr/bin/env python3
"""trace: a tiny local terminal command recorder and log query tool."""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG = Path(os.environ.get("TRACE_LOG", Path.home() / ".trace.json"))


# Return the current time as an unambiguous UTC timestamp.
def now_stamp():
    return datetime.now(timezone.utc).isoformat()


# Read valid log entries, treating a missing or damaged file as an empty log.
def load_log():
    try:
        with LOG.open(encoding="utf-8") as file:
            data = json.load(file)
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


# Atomically replace the log so an interrupted write does not corrupt history.
def save_log(entries):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    temp = LOG.with_suffix(LOG.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)
    temp.replace(LOG)


# Run a typed command in the session directory using the host's normal shell.
def run_command(command, cwd):
    if os.name == "nt":
        return subprocess.run(["powershell", "-NoProfile", "-Command", command], cwd=cwd).returncode
    return subprocess.run(command, shell=True, cwd=cwd).returncode


# Keep a simple interactive shell loop and record every non-empty command line.
def record():
    entries, cwd = load_log(), Path.cwd()
    print("TRACE recorder online. Type exit to stop. Log:", LOG)
    while True:
        try:
            command = input("trace " + str(cwd) + "> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if command.lower() in {"exit", "quit"}:
            break
        if not command:
            continue
        if command == "cd" or command.startswith("cd "):
            target = command[2:].strip().strip('"') or str(Path.home())
            candidate = (cwd / target).resolve() if not Path(target).is_absolute() else Path(target)
            if candidate.is_dir():
                cwd = candidate
            else:
                print("TRACE: directory unavailable.")
            entries.append({"timestamp": now_stamp(), "command": command, "cwd": str(cwd)})
            save_log(entries)
            continue
        entries.append({"timestamp": now_stamp(), "command": command, "cwd": str(cwd)})
        save_log(entries)
        run_command(command, str(cwd))
    print("TRACE recorder offline.")


# Derive a time window from the limited natural phrases supported by this CLI.
def time_window(question):
    text, now = question.lower(), datetime.now(timezone.utc)
    match = re.search(r"(?:last|in the last)\s+(\d+)\s+(minute|hour|day)s?", text)
    if match:
        amount, unit = int(match.group(1)), match.group(2)
        return now - timedelta(**{unit + "s": amount}), now, "the last " + match.group(1) + " " + unit + "s"
    if "last hour" in text:
        return now - timedelta(hours=1), now, "the last hour"
    if "today" in text:
        local = datetime.now().date()
        start = datetime.combine(local, datetime.min.time()).astimezone().astimezone(timezone.utc)
        return start, now, "today"
    return None, now, "all time"


# Answer a count or listing question solely from local command entries.
def ask(question):
    start, end, label = time_window(question)
    entries = []
    for entry in load_log():
        try:
            stamp = datetime.fromisoformat(entry["timestamp"])
            if start is None or start <= stamp <= end:
                entries.append(entry)
        except (KeyError, TypeError, ValueError):
            pass
    count = re.search(r"how many times(?: did i)? run\s+(.+?)(?:\s+(?:today|last|in the last)\b|[?!.,]*$)", question, re.I)
    if count:
        target = count.group(1).strip().strip('"\'').lower()
        total = sum(e.get("command", "").lower() == target or e.get("command", "").lower().startswith(target + " ") for e in entries)
        print("TARS:", total, "instance" + ("" if total == 1 else "s"), "of '" + target + "'", label + ".")
        return
    if not entries:
        print("TARS: No recorded commands match.")
        return
    print("TARS:", len(entries), "command" + ("" if len(entries) == 1 else "s"), "found for", label + ".")
    for entry in entries[-25:]:
        stamp = datetime.fromisoformat(entry["timestamp"]).astimezone().strftime("%Y-%m-%d %H:%M")
        print(stamp + "  " + entry["command"])
    if len(entries) > 25:
        print("TARS: Output limited to the latest 25. Sensible precaution.")


# Empty the local command history after an explicit interactive confirmation.
def clear_history(force=False):
    entries = load_log()
    if not entries:
        print("TARS: History is already empty.")
        return
    if not force:
        try:
            answer = input("TARS: Delete " + str(len(entries)) + " recorded commands? Type CLEAR: ")
        except (EOFError, KeyboardInterrupt):
            answer = ""
        if answer != "CLEAR":
            print("TARS: History retained.")
            return
    save_log([])
    print("TARS: History cleared. Memory is optional.")


# Validate CLI arguments and dispatch to the recorder or local question handler.
def main():
    if len(sys.argv) == 2 and sys.argv[1] == "record":
        record()
    elif len(sys.argv) >= 3 and sys.argv[1] == "ask":
        ask(" ".join(sys.argv[2:]))
    elif len(sys.argv) == 2 and sys.argv[1] == "clear":
        clear_history()
    elif len(sys.argv) == 3 and sys.argv[1:3] == ["clear", "--yes"]:
        clear_history(force=True)
    else:
        print("Usage: trace record | trace ask \"what did I run in the last hour\" | trace clear [--yes]")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
