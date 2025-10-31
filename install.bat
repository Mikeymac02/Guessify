@echo off
REM Robust double-click-friendly installer for Guessify
REM Tries common full paths for the py launcher, then py, then python.
REM Leaves the window open and prints clear manual commands if something fails.

setlocal

REM Common full paths for the Python launcher
set "PY_CANDIDATE_1=C:\Windows\py.exe"
set "PY_CANDIDATE_2=%LOCALAPPDATA%\Programs\Python\Launcher\py.exe"
set "PY_CANDIDATE_3=%ProgramFiles%\Python\Launcher\py.exe"

REM Try full paths first (use the first that exists)
if exist "%PY_CANDIDATE_1%" (
    set "PY_CMD=%PY_CANDIDATE_1%"
) else if exist "%PY_CANDIDATE_2%" (
    set "PY_CMD=%PY_CANDIDATE_2%"
) else if exist "%PY_CANDIDATE_3%" (
    set "PY_CMD=%PY_CANDIDATE_3%"
) else (
    REM Fall back to checking 'py' on PATH
    where py >nul 2>&1
    if %ERRORLEVEL%==0 (
        set "PY_CMD=py"
    ) else (
        where python >nul 2>&1
        if %ERRORLEVEL%==0 (
            set "PY_CMD=python"
        ) else (
            set "PY_CMD="
        )
    )
)

if defined PY_CMD (
    echo Using launcher: %PY_CMD%
    REM Use -3 to force Python 3
    "%PY_CMD%" -3 -m venv env
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to create virtual environment using %PY_CMD%.
        echo You can try the manual commands shown below.
        pause
        goto MANUAL_INSTRUCTIONS
    )

    echo Created virtual environment: env\
    echo Activating...
    call env\Scripts\activate.bat
    if %ERRORLEVEL% NEQ 0 (
        echo Failed to auto-activate the virtual environment.
        echo If you are using PowerShell, run: .\env\Scripts\Activate.ps1
        pause
        goto MANUAL_INSTRUCTIONS
    )

    echo Upgrading pip...
    python -m pip install --upgrade pip

    if exist requirements.txt (
        echo Installing dependencies from requirements.txt...
        pip install -r requirements.txt
        if %ERRORLEVEL% NEQ 0 (
            echo pip install failed. See the output above for details.
            pause
            goto MANUAL_INSTRUCTIONS
        )
    ) else (
        echo requirements.txt not found - skipping dependency installation.
    )

    echo.
    echo Setup finished successfully.
    echo To run the game:
    echo    env\Scripts\activate
    echo    python main.py
    pause
    exit /b 0
)

:MANUAL_INSTRUCTIONS
echo.
echo Could not locate a usable Python launcher or venv setup failed.
echo Copy and paste these commands into a Command Prompt (not PowerShell) opened in this folder:
echo ----------------------------------------------------
echo py -3 -m venv env
echo env\Scripts\activate
echo python -m pip install --upgrade pip
echo pip install -r requirements.txt
echo python main.py
echo ----------------------------------------------------
echo If 'py' is not found, install Python from https://www.python.org/downloads and make sure:
echo  - "Install launcher for all users (recommended)" is selected
echo  - "Add Python to PATH" is checked
echo
echo Tip: If double-clicking still fails, open Command Prompt, cd to this folder, and run install.bat from there.
pause
start cmd /k "echo Manual commands to run in this folder & echo -------------------------------- & echo cd %cd% & echo py -3 -m venv env & echo env\Scripts\activate & echo python -m pip install --upgrade pip & echo pip install -r requirements.txt & echo python main.py & cmd"

endlocal
