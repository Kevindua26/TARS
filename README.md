# TARS / Trace 🤖⏱️

> **A tiny, zero-dependency terminal command recorder and natural language history query tool with a dash of TARS personality.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20(Stdlib)-brightgreen.svg)]()

Ever find yourself wondering *"What on earth did I run 20 minutes ago to get this build passing?"* or *"How many times did I push to main today?"*

**TARS (Trace)** records your terminal sessions in real time into an atomic local log and lets you ask natural-language questions about your command history—completely offline, private, and with zero third-party dependencies.

---

## ✨ Features

- **🎙️ Seamless Session Recording**: Launches an interactive shell wrapper that records commands, timestamps (UTC), and execution working directories.
- **💬 Natural Language Querying**: Query your history using intuitive time frames (*"in the last 2 hours"*, *"today"*, *"last 30 minutes"*).
- **📊 Frequency & Count Analytics**: Ask questions like *"how many times did I run git commit today?"*.
- **🔒 100% Local & Privacy-First**: No servers, no telemetry, no API keys. All data is saved strictly to your local machine.
- **🛡️ Atomic Writes**: Uses atomic rename (`.tmp` → log file) to prevent log corruption even if interrupted abruptly.
- **⚡ Zero External Dependencies**: Built entirely using Python's standard library (`subprocess`, `re`, `datetime`, `pathlib`, `json`).
- **💻 Cross-Platform**: Native execution using PowerShell on Windows and standard shell on Linux/macOS.

---

## 🚀 Quick Start

### 1. Requirements
- Python 3.8 or higher.

### 2. Clone the Repository
```bash
git clone https://github.com/Kevindua26/TARS.git
cd TARS
```

### 3. (Optional) Set Up a Global Shortcut / Alias

To use `trace` from anywhere in your terminal:

**Linux / macOS (Bash/Zsh):**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
alias trace="python3 /path/to/TARS/trace.py"
```

**Windows (PowerShell):**
Add to your PowerShell `$PROFILE`:
```powershell
function trace { python "D:\Work\Pvt\Project\TARS\trace.py" @args }
```

---

## 📖 Usage

### 1. Record an Interactive Terminal Session

Start the recorder:
```bash
python trace.py record
```

Inside the recorder shell:
```text
TRACE recorder online. Type exit to stop. Log: C:\Users\you\.trace.json
trace C:\Projects\demo> git status
trace C:\Projects\demo> npm run build
trace C:\Projects\demo> cd ..
trace C:\Projects> exit
TRACE recorder offline.
```

- Navigation with `cd` updates the active session directory dynamically.
- Type `exit` or `quit` (or press `Ctrl+C` / `Ctrl+D`) to exit.

---

### 2. Query Your History (`ask`)

Ask questions about what you ran and when:

#### View Recent Commands by Time Window
```bash
python trace.py ask "what did I run in the last hour"
python trace.py ask "commands run in the last 30 minutes"
python trace.py ask "what did I do today"
```

**Sample Output:**
```text
TARS: 4 commands found for the last hour.
2026-09-09 17:42  git status
2026-09-09 17:45  pytest tests/
2026-09-09 17:50  git add .
2026-09-09 17:51  git commit -m "fix: resolve edge case in parser"
```

#### Count Specific Command Runs
```bash
python trace.py ask "how many times did I run pytest today?"
python trace.py ask "how many times did I run git push in the last 2 hours"
```

**Sample Output:**
```text
TARS: 6 instances of 'pytest' today.
```

---

### 3. Clear History (`clear`)

Safely wipe your recorded command history:

```bash
python trace.py clear
```

Prompts for an explicit confirmation before deletion:
```text
TARS: Delete 142 recorded commands? Type CLEAR: CLEAR
TARS: History cleared. Memory is optional.
```

To skip the interactive confirmation (e.g. in CI or scripts):
```bash
python trace.py clear --yes
```

---

## ⚙️ Configuration

By default, TARS writes logs to:
- **Default path:** `~/.trace.json` (inside your user home directory)

You can customize the log path at any time using the `TRACE_LOG` environment variable:

```bash
# Linux / macOS
export TRACE_LOG="/custom/path/my_commands.json"

# Windows (PowerShell)
$env:TRACE_LOG = "D:\Logs\my_commands.json"
```

### Log Format
Each record is saved as structured JSON:
```json
[
  {
    "timestamp": "2026-09-09T12:45:00.123456+00:00",
    "command": "git pull origin main",
    "cwd": "/path/to/project"
  }
]
```

---

## 🛠️ CLI Reference

| Command | Description |
| :--- | :--- |
| `trace record` | Launch the interactive recording shell session |
| `trace ask "<phrase>"` | Search and query command history with natural time phrases |
| `trace clear` | Interactively clear all recorded history (prompts for `CLEAR`) |
| `trace clear --yes` | Force clear recorded history without confirmation prompt |

---

## 🤝 Contributing

Contributions, feedback, and ideas are welcome!
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/cool-feature`)
3. Commit your changes (`git commit -m "feat: add support for regex search"`)
4. Push to the branch (`git push origin feature/cool-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) - feel free to use and adapt as you see fit.
