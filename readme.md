# Criar um ambiente virtual (Linux/macOS)
python3 -m venv venv

# Ativar o ambiente virtual no Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Execute project
uvicorn main:app --reload