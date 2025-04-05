@echo off

REM Run the FastAPI + React app via uvicorn (global env)
uvicorn main:app --host 127.0.0.1 --port 8088
pause
