@echo off
git add .
set /p msg="请输入本次更新说明: "
git commit -m "%msg%"
git push
pause