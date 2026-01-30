@echo off
echo 🚀 Launching Local LLM Testcase Generator...
echo ⚡ Ensuring Ollama is running...
tasklist /FI "IMAGENAME eq ollama.exe" 2>NUL | find /I /N "ollama.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Ollama is running.
) else (
    echo ⚠️ Ollama is NOT running. Please start Ollama Desktop first.
    pause
    exit /b
)

echo 🧪 Starting Streamlit App...
call .venv\Scripts\activate
streamlit run app.py
pause
