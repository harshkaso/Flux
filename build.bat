@echo off
setlocal

REM --- Configuration ---
set APP_NAME=Flux
set ENTRY_POINT=flux\__main__.py
set VENV_NAME=venv_build
set DIST_DIR=dist
set OUTPUT_NAME=%APP_NAME%_Windows.exe

echo Building for Windows, output name: %OUTPUT_NAME%

REM --- Setup Virtual Environment ---
if not exist "%VENV_NAME%\Scripts\activate.bat" (
    echo Creating virtual environment: %VENV_NAME%
    python -m venv "%VENV_NAME%"
) else (
    echo Virtual environment %VENV_NAME% already exists.
)

echo Activating virtual environment...
call "%VENV_NAME%\Scripts\activate.bat"

REM --- Install/Upgrade Build Tools and Dependencies ---
echo Upgrading pip...
python -m pip install --upgrade pip

echo Installing Nuitka, setuptools, and wheel...
pip install nuitka setuptools wheel

echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM --- Create Distribution Directory ---
if not exist "%DIST_DIR%" (
    echo Creating directory: %DIST_DIR%
    mkdir "%DIST_DIR%"
)

REM --- Run Nuitka ---
echo Running Nuitka to build the executable...

REM Nuitka options
REM Using --mingw64 by default, ensure MinGW64 (e.g., via MSYS2) is in PATH or Nuitka can find it.
REM Use --windows-disable-console for GUI applications.
python -m nuitka ^
    --onefile ^
    --output-dir="%DIST_DIR%" ^
    --output-filename="%OUTPUT_NAME%" ^
    --enable-plugin=numpy ^
    --include-data-dir=assets=assets ^
    --include-data-dir=flux\Space_Mono=flux\Space_Mono ^
    --windows-disable-console ^
    --mingw64 ^
    "%ENTRY_POINT%"

if %errorlevel% neq 0 (
    echo Nuitka build failed.
    exit /b %errorlevel%
)

echo Build process completed.
echo Executable should be in %DIST_DIR%\%OUTPUT_NAME%

REM --- Deactivate Virtual Environment (optional) ---
REM echo Deactivating virtual environment.
REM call deactivate

endlocal
exit /b 0
