# Claude Prompt Templates

This folder contains **reusable prompt templates** for interacting with Claude or any LLM in your local CLI workflow.

## Purpose

The templates are designed to turn `@intent` comments in your code into **machine-readable instructions** for Claude.  
They allow the model to:

- Summarize what a folder or module does.
- Explain individual functions or files.
- Provide context-aware guidance based on your codebase.

## Folder Structure

```
.claude/prompts/
├── folder\_summary.txt      # Template for summarizing a folder based on @intent comments
├── function\_summary.txt    # Template for summarizing a single function or file
└── README.md               # This documentation
```

## Usage

1. Extract `@intent` comments from your code using your intent finder tool.
2. Retrieve the top-k relevant intents for a folder or file.
3. Load the desired template (e.g., `folder_summary.txt`).
4. Replace placeholders like `{folder_name}` and `{intents}` with actual values.
5. Send the filled prompt to Claude via API or OpenRouter endpoint.

Example in Python:

```python
with open(".claude/prompts/folder_summary.txt") as f:
    template = f.read()

filled_prompt = template.format(
    folder_name="src/auth",
    intents="\n".join([i['intent'] for i in top_k_intents])
)

response = claude_api.send(filled_prompt)
print(response)
````

## Adding New Templates

* Create a new `.txt` file in this folder.
* Use placeholders (`{folder_name}`, `{intents}`, `{function_name}`) for dynamic substitution.
* Keep the prompt **clear, concise, and focused** on what you want the AI to do.

