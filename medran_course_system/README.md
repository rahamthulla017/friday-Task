# Medran Course System — Local Run Instructions

Minimal instructions to get the project running locally on Windows (PowerShell). These commands assume you have Python 3.11+ installed and available as `python` on PATH.

1) Create a virtual environment and activate it (optional: activate to run commands without full path)

```powershell
# create venv
python -m venv .venv

# activate in PowerShell (if ExecutionPolicy allows)
.\.venv\Scripts\Activate.ps1

# alternatively, run python from the venv without activating:
.\.venv\Scripts\python -m pip install -U pip setuptools wheel
```

2) Install dependencies

```powershell
.\.venv\Scripts\python -m pip install -r requirements.txt
```

3) Apply migrations and create a superuser (optional)

```powershell
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py createsuperuser
```

4) Run the development server

```powershell
.\.venv\Scripts\python manage.py runserver 8000
# open http://127.0.0.1:8000/ in your browser
```

5) Run tests

```powershell
.\.venv\Scripts\python manage.py test
```

Notes
- The project uses SQLite (db.sqlite3) by default — no DB server required for local dev.
- `settings.py` has DEBUG=True and a development SECRET_KEY — do not use these in production.
- The registration endpoint is at `/api/register/` and returns JWT access/refresh tokens using SimpleJWT.

Troubleshooting
- If activating the venv in PowerShell fails due to execution policy, you can either run commands with the venv Python directly (i.e., `.\.venv\Scripts\python manage.py runserver`) or allow script execution temporarily using `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`.
