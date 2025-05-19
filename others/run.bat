@echo off
:: 检查是否以管理员身份运行
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo administrator power needed.
    pause
    exit
)

:: 获取当前 bat 文件所在的目录
set "BASE_DIR=%~dp0"

:: 在第一个 CMD 窗口中运行 Flask 应用（使用虚拟环境）
start cmd /k "cd /d %BASE_DIR%backend && python app.py"

:: 在第二个 CMD 窗口中运行 Vue 前端
start cmd /k "cd /d %BASE_DIR%frontend && npm run serve"

:: 在第三个 CMD 窗口中运行 CosyVoice 后端
start cmd /k "cd /d E:\Program\CosyVoice && conda activate cosyvoice && python server.py"

:: 结束脚本
exit
