@echo off
cd /d %~dp0

echo Активируем виртуальное окружение...
call C:\venvs\stroikontrol\Scripts\activate.bat

echo Запуск сервера FastAPI...
uvicorn app.main:app --reload

pause
