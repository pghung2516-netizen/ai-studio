@echo off
chcp 65001 >nul
title TTOMORROW STUDIO - Cai dat
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\cai-dat.ps1"
echo.
pause
