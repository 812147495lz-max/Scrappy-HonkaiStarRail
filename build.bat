@echo off
chcp 65001
cls
echo ==========================================
echo        正在准备将 Python 封装为 Exe
echo ==========================================

REM 1. 检查并安装 PyInstaller (如果已有则会跳过)
echo [1/3] 正在检查 PyInstaller 环境...
pip install pyinstaller

REM 2. 开始打包
REM --onefile: 打包成单个exe文件，而不是一个文件夹
REM --clean: 清除缓存
REM --name: 指定生成的exe名字
echo.
echo [2/3] 正在打包 Scrappy-HonkaiStarRail.py ...
echo 请耐心等待，可能需要几十秒...

pyinstaller --onefile --clean --name "HonkaiStarRail_Game" Scrappy-HonkaiStarRail.py

echo.
echo ==========================================
if exist "dist\HonkaiStarRail_Game.exe" (
    echo [3/3] 打包成功！
    echo.
    echo 你的 exe 文件在当前目录下的 [dist] 文件夹里。
    echo 正在为你打开文件夹...
    start dist
) else (
    echo [!] 打包失败，请检查报错信息。
)
echo ==========================================
pause