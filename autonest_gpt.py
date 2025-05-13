# autonest_gpt.py

import openai
import os

# API-Schlüssel setzen (nur wenn bereit)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Alternativ direkt einfügen

def build_prompt(code_str, project_structure_summary):
    """
    Erstellt den Prompt für GPT, um zu bewerten, wohin der Code gehören sollte.
    """
    return f"""
Du bist ein semantisch orientierter Code-Assistent.

Hier ist ein neuer Codeblock, den der Nutzer einfügen möchte:

```python
{code_str}


def describe_project_with_gpt(project_path):
    import os
    from openai import ChatCompletion

    summary_input = ""
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, encoding="utf-8") as f:
                    content = f.read()
                    summary_input += f"# Datei: {file}\n" + content[:1500] + "\n\n"  # Kürzung auf max GPT-Kontext

    messages = [
        {"role": "system", "content": "Du bist ein Code-Analyst. Beschreibe kurz, was dieses Projekt tut."},
        {"role": "user", "content": summary_input}
    ]

    response = ChatCompletion.create(model="gpt-4", messages=messages)
    return response["choices"][0]["message"]["content"]
