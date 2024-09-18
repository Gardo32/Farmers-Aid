import os

deps = ['streamlit', 'pandas','requests','python-dotenv','plotly','pycountry']

os.system("pip install uv")

for dep in deps:
    os.system("uv pip install " + dep)
