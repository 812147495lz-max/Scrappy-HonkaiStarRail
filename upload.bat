@echo off
chcp 65001 >nul
color 0a
cls
echo ==========================================
echo        [Scrappy-HSR] 智能同步上传脚本
echo ==========================================

REM --- 第一步：保存本地修改 ---
echo.
echo [1/3] 正在保存本地修改...
git add .
set /p msg="请输入更新描述 (回车默认: 代码优化): "
if "%msg%"=="" set msg="代码优化"
git commit -m "%msg%"

REM --- 第二步：拉取云端更新 (关键步骤) ---
echo.
echo [2/3] 正在拉取云端代码并合并...
echo ------------------------------------------
git pull origin main

REM 错误检测：如果拉取出现冲突，脚本变红并暂停
if %errorlevel% neq 0 (
    color 0c
    echo.
    echo ==========================================
    echo [X] 发生冲突或错误！
    echo [!] 请手动打开文件解决冲突 (查找 ^<^<^<^<^<^< HEAD)。
    echo [!] 解决完冲突后，请重新运行此脚本。
    echo ==========================================
    pause
    exit /b
)

REM --- 第三步：上传到云端 ---
echo.
echo [3/3] 正在将最终结果上传到 GitHub...
echo ------------------------------------------
git push origin main

REM 错误检测：如果上传失败
if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [X] 上传失败！请检查网络或代理设置。
    pause
    exit /b
)

echo.
echo -------------------------------
echo [Scrappy-HSR] 同步 & 上传全部成功！
pause