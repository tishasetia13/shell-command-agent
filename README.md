# shell-command-agent

A small AI agent that lives in the terminal. You describe what you want in plain English, and it writes the shell command, shows it to you, and runs it only after you approve.

I built this from scratch in pure Python (no agent frameworks) to learn how AI agents work and to get better at command-line basics.

## How it works

1. You type a request, like `ai "make a folder called notes"`.
2. The model decides which shell command does that.
3. The program shows you the command and asks `Run this? (y/n)`.
4. If you type `y`, the command runs and the output goes back to the model, which can then run another command or give you a final answer.

This approval step is called human in the loop: a person checks every action before it happens.

## Setup

1. Clone the repo and go into the folder.

```
git clone https://github.com/tishasetia13/shell-command-agent.git
cd shell-command-agent
```

2. Create a virtual environment and install the requirements.

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a file called `.env` in the project folder with your Anthropic API key.

```
ANTHROPIC_API_KEY=your-key-here
```

## Usage

```
python agent.py "show me what is in this folder"
```

To call it from any folder, add an alias to your `~/.zshrc` that points to your venv's Python and to `agent.py`, using the full paths on your computer:

```
alias ai='/full/path/to/.venv/bin/python /full/path/to/agent.py'
```

Then you can type `ai "your request"` anywhere.

## Notes

- This is a learning project. It runs real commands on your computer, so read each proposed command before you type `y`.
- Built with the Anthropic API and Python's `subprocess` module.
