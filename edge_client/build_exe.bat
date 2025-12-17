@echo off
echo ========================================================
echo  ScreenWatcher - EXE Builder
echo ========================================================

REM Sprawdzenie czy Python jest zainstalowany
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo BLAD: Python nie jest zainstalowany lub nie ma go w PATH.
    pause
    exit /b
)

echo.
echo 1. Tworzenie wirtualnego srodowiska (opcjonalne, ale bezpieczne)...
if not exist ".venv" (
    python -m venv .venv
)

echo.
echo 2. Aktywacja srodowiska...
call .venv\Scripts\activate

echo.
echo 3. Instalacja zaleznosci...
pip install -r requirements.txt
pip install pyinstaller

echo.
echo 4. Budowanie pliku EXE (One File)...
echo To moze potrwac chwile...
pyinstaller --onefile --name ScreenWatcher main.py

echo.
echo ========================================================
echo  SUKCES!
echo  Twoj plik znajduje sie w folderze: dist\ScreenWatcher.exe
echo ========================================================
pause
