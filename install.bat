@echo off
echo 🚀 Support Agent Installation Script (Windows)
echo ============================================

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set python_version=%%i
echo ✅ Python found: %python_version%

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "support_agent_env" (
    python -m venv support_agent_env
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call support_agent_env\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

REM Check for API key
echo.
echo Checking for Gemini API key...
if "%GEMINI_API_KEY%"=="" (
    echo ⚠️  GEMINI_API_KEY environment variable not set
    echo    Please set your Gemini API key:
    echo    set GEMINI_API_KEY=your_api_key_here
    echo.
    echo    Or update the config.py file with your API key
) else (
    echo ✅ Gemini API key found
)

REM Run health check
echo.
echo Running health check...
python main.py --health-check
if %errorlevel% neq 0 (
    echo.
    echo ❌ Health check failed. Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo Quick start commands:
echo   python main.py                    # Run default example
echo   python main.py --test             # Run test scenarios
echo   python main.py --interactive      # Interactive mode
echo   python main.py --help             # Show all options
echo.
pause
