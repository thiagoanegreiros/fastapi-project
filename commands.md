
# Activate Environment
source .venv/bin/activate

# Install dependencies
uv sync

# Execute project
uvicorn main:app --reload

# execute on server
export PORT=8001 && uvicorn main:app --host=0.0.0.0 --port=${PORT}

# Execute manual pre commit
pre-commit run --all-files
