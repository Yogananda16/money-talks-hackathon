import subprocess
import sys

steps = [
    "extract_questions.py",
    "search_documents.py",
    "build_profile.py",
    "ask_loop.py",
    "conflict_check.py",
    "generate_report.py"
]

for step in steps:
    print(f"\n{'='*50}\nRunning {step}\n{'='*50}\n")
    result = subprocess.run([sys.executable, step])
    if result.returncode != 0:
        print(f"\n{step} failed — stopping pipeline.")
        break