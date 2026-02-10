@echo off
chcp 65001 >nul
git add .
set /p msg="请输入更新描述: "
if "%msg%"=="" set msg="代码优化"
git commit -m "%msg%"
git push origin main
echo -------------------------------
echo [Scrappy-HSR] 上传成功！
pause