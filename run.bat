@echo off
REM Marsool Al-Barq - start the system locally (no Docker needed)
cd /d "%~dp0"
set TAILWINDCSS_VERSION=v4.3.3
set PYTHONUTF8=1
where uv >/dev/null 2>/dev/null && (set UV=uv) || (set UV=python -m uv)
echo [1/5] Installing packages...
%UV% sync --quiet || goto :error
echo [2/5] Starting database...
.venv\Scripts\python scripts\devdb.py start || goto :error
echo [3/5] Building styles...
.venv\Scripts\tailwindcss -i static\src\app.css -o static\css\app.css --minify || goto :error
echo [4/5] Updating database...
.venv\Scripts\python manage.py migrate --noinput || goto :error
.venv\Scripts\python manage.py seed_org || goto :error
echo.
echo   [5/5] Marsool Al-Barq is running:  http://127.0.0.1:8000
echo   Keep this window open. Press Ctrl+C to stop.
echo.
start "" http://127.0.0.1:8000
.venv\Scripts\python manage.py runserver 127.0.0.1:8000
goto :eof
:error
echo.
echo   Something failed. Scroll up to see the error, and send a screenshot.
pause
