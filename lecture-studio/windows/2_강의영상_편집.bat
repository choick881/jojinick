@echo off
chcp 65001 >nul
title HY FLIP 강의 편집기
set "ROOT=%~dp0.."
set "PATH=%ROOT%\tools\ffmpeg\bin;%PATH%"
set "PYTHONUTF8=1"
if not exist "%ROOT%\.venv\Scripts\python.exe" (
  echo 먼저 windows 폴더의 1_설치하기.bat 을 실행하세요.
  pause
  exit /b 1
)
"%ROOT%\.venv\Scripts\python.exe" "%ROOT%\engine\studio.py" %*
echo.
pause
