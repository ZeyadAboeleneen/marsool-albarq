@echo off
REM مرسول البرق — تشغيل النظام على الجهاز (من غير Docker)
cd /d "%~dp0"
set TAILWINDCSS_VERSION=v4.3.3
where uv >nul 2>nul && (set UV=uv) || (set UV=python -m uv)
%UV% sync --quiet || goto :error
.venv\Scripts\python scripts\devdb.py start || goto :error
.venv\Scripts\tailwindcss -i static\src\app.css -o static\css\app.css --minify || goto :error
.venv\Scripts\python manage.py migrate --noinput || goto :error
.venv\Scripts\python manage.py seed_org || goto :error
echo.
echo   Marsool Al-Barq is running:  http://127.0.0.1:8000
echo.
.venv\Scripts\python manage.py runserver 127.0.0.1:8000
goto :eof
:error
echo.
echo   Something failed. Scroll up to see the error.
pause
