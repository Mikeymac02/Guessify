@echo off
REM Windows install script: creates venv, activates and installs deps

REM Check python exists
python --version >nul 2>&1
IF ERRORLEVEL 1 (
  echo Python not found. Install Python 3.8+ and add to PATH.
  pause
  exit /b 1
)

REM Create virtual environment
python -m venv env

echo Creating virtual environment in .\env
if not exist env (
  echo Failed to create venv.
  pause
  exit /b 1
)

REM Activate and install
call env\Scripts\activate.bat
IF ERRORLEVEL 1 (
  echo Failed to activate virtual environment.
  pause
  exit /b 1
)

echo Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo
echo Setup complete. To run the game:
echo    env\Scripts\activate
echo    python main.py
pause
