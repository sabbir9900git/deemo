# Windows Setup & Execution Guide (PowerShell & Command Prompt)

Follow these exact commands to install, initialize, and run **MARS EXPLORER** on Windows 10 or Windows 11.

## 1. Copy Environment File
```powershell
copy .env.example .env
```

## 2. Install Python Backend Dependencies
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

## 3. Initialize SQLite Database & Import USGS Mars Place Names
```powershell
python scripts\init_db.py
python scripts\import_usgs_nomenclature.py
```

## 4. Start the FastAPI Backend Server
```powershell
cd backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 5. Install & Start the Next.js Frontend (New Terminal Window)
```powershell
cd frontend
npm install
npm run dev
```

## 6. Run the Application
Open **`http://localhost:3000`** in Microsoft Edge, Chrome, or Firefox.
