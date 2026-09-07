import os
from dotenv import load_dotenv
load_dotenv()  # reads src/.env

import litellm
from prismtrace import install_litellm

# One call at startup — do NOT wrap individual calls with this
install_litellm(
    api_key=os.environ["PRISMTRACE_API_KEY"],
    project_id=os.environ["PRISMTRACE_PROJECT_ID"],
)

def ask_ollama(prompt, model="ollama/qwen3:4b"):
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        api_base="http://localhost:11434",
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print(ask_ollama("Say hello in one short sentence."))