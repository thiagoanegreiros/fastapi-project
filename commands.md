
# Activate Environment
source .venv/bin/activate

# Install hooks
pre-commit install --install-hooks

# Install dependencies
uv sync

# Execute project
uvicorn main:app --reload

# execute on server
uv run uvicorn main:app --host=0.0.0.0 

# Execute manual pre commit
pre-commit run --all-files

# Execute this to run on Render
uv pip freeze > requirements.txt