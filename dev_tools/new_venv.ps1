# Use when a venv doesn't exist
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -Ue .[dev]
