import json

def parse_claude_logs(log_file, output_file):
    """
    Parses a claude-logs.jsonl file and writes the conversation to a Markdown file.

    Args:
        log_file (str): The path to the log file.
        output_file (str): The path to the output Markdown file.
    """
    with open(output_file, 'w') as md_file:
        md_file.write("# Claude Conversation Log\n\n")
        try:
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        log_entry = json.loads(line)
                        message_type = log_entry.get("type")
                        message = log_entry.get("message", {})
                        content = ""

                        if message_type == "user":
                            md_file.write("## User\n\n")
                            if "content" in message:
                                if isinstance(message["content"], list):
                                    for item in message["content"]:
                                        if isinstance(item, dict) and item.get("type") == "text":
                                            md_file.write(f'{item.get("text", "")}\n')
                                        elif isinstance(item, str):
                                            md_file.write(f"{item}\n")
                                else:
                                    md_file.write(f'{message.get("content", "")}\n')
                            md_file.write("\n")

                        elif message_type == "assistant":
                            md_file.write("## Assistant\n\n")
                            if "content" in message:
                                if isinstance(message["content"], list):
                                    for item in message["content"]:
                                        if isinstance(item, dict):
                                            if item.get("type") == "text":
                                                md_file.write(f'{item.get("text", "")}\n')
                                            elif item.get("type") == "tool_use":
                                                tool_name = item.get("name")
                                                tool_input = item.get("input")
                                                md_file.write(f"**Tool Used:** `{tool_name}`\n\n")
                                                md_file.write("````json\n")
                                                md_file.write(json.dumps(tool_input, indent=2))
                                                md_file.write("\n````\n\n")
                                        elif isinstance(item, str):
                                            md_file.write(f"{item}\n")
                                else:
                                    md_file.write(f'{message.get("content", "")}\n')
                            md_file.write("\n")

                    except json.JSONDecodeError:
                        # Ignore lines that are not valid JSON
                        pass
        except FileNotFoundError:
            print(f"Error: Log file not found at {log_file}")

if __name__ == "__main__":
    parse_claude_logs("claude-logs.jsonl", "claude_logs.md")