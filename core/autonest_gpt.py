import os
from openai import ChatCompletion

openai_api_key = os.getenv("OPENAI_API_KEY")


def build_prompt(code_str, project_structure_summary):
    return f"""Du bist ein semantisch orientierter Code-Assistent.

Hier ist ein neuer Codeblock, den der Nutzer einfügen möchte:

```python
{code_str}
```

Basierend auf dieser Projektstruktur:
{project_structure_summary}

Bitte bewerte:
- in welche Datei dieser Code gehört,
- ob er eine Funktion erweitern oder eine neue anlegen soll,
- und wie sicher du dir dabei bist.
"""


def describe_project_with_gpt(project_path):
    import os

    summary_input = ""
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                    summary_input += f"# Datei: {file}\n" + content[:1500] + "\n\n"

    messages = [
        {
            "role": "system",
            "content": "Du bist ein Code-Analyst. Beschreibe kurz, was dieses Projekt tut.",
        },
        {"role": "user", "content": summary_input},
    ]

    response = ChatCompletion.create(model="gpt-4", messages=messages, api_key=openai_api_key)
    return response["choices"][0]["message"]["content"]
