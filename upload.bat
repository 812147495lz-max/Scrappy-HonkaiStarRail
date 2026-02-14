@echo off
chcp 65001
color 0a
cls
echo ==========================================
echo        [Scrappy-HSR] 强力调试版
echo   (不管发生什么，这个窗口都不会自动关闭)
echo ==========================================

REM --- 第一步：保存本地修改 ---
echo.
echo [1/3] 正在保存本地修改...
git add .
set /p msg="请输入更新描述 (回车默认: 代码优化): "
if "%msg%"=="" set msg="代码优化"
git commit -m "%msg%"

echo.
echo ------------------------------------------
echo [暂停] 马上要开始拉取(Pull)代码了。
echo 如果这里闪退，说明是 git pull 命令本身导致的问题。
echo 请按任意键继续...
pause
echo ------------------------------------------

REM --- 第二步：拉取云端更新 ---
echo.
echo [2/3] 正在拉取云端代码...
echo 正在执行: git pull origin main
echo ------------------------------------------

REM 这里去掉了错误检测的自动退出，改为显示错误信息但不关闭
git pull origin main

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo ==========================================
    echo [!!!] 警告：拉取/合并出现问题！[!!!]
    echo.
    echo 常见原因：
    echo 1. 发生冲突 (Conflict)：需要手动打开文件解决冲突。
    echo 2. 拒绝合并 (Refusing to merge)：历史记录不匹配。
    echo.
    echo 请向上滚动查看红色的 git 报错信息！
    echo ==========================================
    echo.
    echo 为了防止数据丢失，脚本将暂停在这里。
    echo 请解决问题后，手动关闭窗口。
    pause
    goto :EOF
)

echo.
echo [成功] 拉取完成。
echo ------------------------------------------

REM --- 第三步：上传到云端 ---
echo.
echo [3/3] 正在上传到 GitHub...
git push origin main

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [X] 上传失败！可能是网络问题。
    pause
    goto :EOF
)

echo.
echo -------------------------------
echo [Scrappy-HSR] 所有操作成功完成！
pause