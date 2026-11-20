@echo off
chcp 65001 >nul
title HY FLIP 강의 편집기 - 설치
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
echo.
pause
