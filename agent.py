import anthropic
from dotenv import load_dotenv
import subprocess
import sys

load_dotenv() 
client = anthropic.Anthropic()

tools = [{
    "name": "run_shell_command",
    "description": "Runs one shell command on the user's computer after the user approves it. Use this whenever the user wants to do something in the terminal, like making folders, running git commands, or starting a project.",
    "input_schema": {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The exact shell command to run, for example: mkdir notes"
            }
        },
        "required": ["command"]
    }
}]

def run_shell_command(command):
    
    print(f"\nProposed command: {command}")
    answer = input("Run this? (y/n): ").strip().lower()

    if answer != "y":
        return "The user declined to run this command."

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output = result.stdout + result.stderr
    print(output)
    return output or "Command ran with no output."


def run_agent(task):
    messages = [{'role': 'user', 'content': task}]
    steps = 0

    while steps < 10:
        steps += 1
        response = client.messages.create(
            model="claude-haiku-5-5",
            max_tokens=1000,
            tools=tools,
            messages=messages,
        )
        if response.stop_reason != 'tool_use':
            return response.content[0].text

        messages.append({'role': 'assistant', 'content': response.content})

        results = []
        for block in response.content:
            if block.type == 'tool_use':
                answer = run_shell_command(block.input['command'])
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": answer,
                })
        
        messages.append({'role': 'user', 'content': results})

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python agent.py "what you want to do"')
    else:
        task = " ".join(sys.argv[1:])
        result = run_agent(task)
        print(result)