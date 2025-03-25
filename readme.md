# Create an Environment
python3 -m venv venv

# Activate Environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Execute project
uvicorn main:app --reload

#execute on server
export PORT=8001 && uvicorn main:app --host=0.0.0.0 --port=${PORT}
