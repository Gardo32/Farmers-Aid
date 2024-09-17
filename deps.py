import os

deps = ['streamlit', 'pandas','requests','python-dotenv']

os.system("pip install uv")

for dep in deps:
    os.system("uv pip install " + dep)
