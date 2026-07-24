@echo off
chcp 936 >nul
setlocal enabledelayedexpansion

title Fleeting Bloom Chronicles - GitHub Pages Upload

echo ============================================================
echo   Fleeting Bloom Chronicles - GitHub Pages 上传工具
echo ============================================================
echo.

:: ====== 检查 Git 是否安装 ======
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git，请先安装 Git for Windows。
    echo 下载地址: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

echo [1/7] Git 已安装 OK
echo.

:: ====== 输入仓库地址 ======
set /p REPO_URL="请输入你的 GitHub 仓库地址（如 https://github.com/用户名/fleeting-bloom-chronicles.git）: "

if "%REPO_URL%"=="" (
    echo [错误] 仓库地址不能为空！
    pause
    exit /b 1
)

echo.
echo 仓库地址: %REPO_URL%
echo.

:: ====== 初始化 Git 仓库（如果还没有的话）======
if not exist ".git" (
    echo [2/7] 初始化 Git 仓库...
    git init
    if %errorlevel% neq 0 (
        echo [错误] git init 失败！
        pause
        exit /b 1
    )
) else (
    echo [2/7] Git 仓库已存在，跳过初始化 OK
)
echo.

:: ====== 设置 Git 用户信息（仅本仓库）======
:: 检查是否已有全局配置，没有就设置本地配置
for /f "tokens=*" %%i in ('git config user.name 2^>nul') do set HAS_NAME=%%i
if "%HAS_NAME%"=="" (
    echo [3/7] 设置 Git 用户信息...
    set /p GIT_NAME="  请输入你的 GitHub 用户名: "
    set /p GIT_EMAIL="  请输入你的 GitHub 邮箱: "
    git config user.name "!GIT_NAME!"
    git config user.email "!GIT_EMAIL!"
) else (
    echo [3/7] Git 用户信息已配置 OK (%HAS_NAME%)
)
echo.

:: ====== 添加文件 ======
echo [4/7] 添加文件...
git add -A
if %errorlevel% neq 0 (
    echo [错误] git add 失败！
    pause
    exit /b 1
)
echo       文件已暂存 OK
echo.

:: ====== 提交 ======
echo [5/7] 创建提交...
git commit -m "feat: initial release of Fleeting Bloom Chronicles"
if %errorlevel% neq 0 (
    echo [提示] 没有新改动需要提交，或提交失败。
    echo        如果你之前已经提交过，这行是正常的。
)
echo.

:: ====== 设置远程仓库并推送 ======
echo [6/7] 推送到 GitHub...
git branch -M main

:: 检查远程是否已配置
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    git remote add origin "%REPO_URL%"
) else (
    git remote set-url origin "%REPO_URL%"
)

git push -u origin main
if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo  [推送失败] 可能的原因：
    echo.
    echo  1. 仓库地址写错了
    echo  2. 需要登录 GitHub（首次推送会弹窗，登录即可）
    echo  3. 仓库不为空且有冲突（去 GitHub 删掉仓库重建空的）
    echo.
    echo  如果弹出登录窗口，登录后重新运行本脚本即可。
    echo ============================================================
    pause
    exit /b 1
)

echo.
echo [7/7] 推送成功 OK
echo.
echo ============================================================
echo   上传完成！
echo ============================================================
echo.
echo   接下来开启 GitHub Pages：
echo.
echo   1. 打开你的 GitHub 仓库页面
echo   2. 点击 Settings（设置）
echo   3. 左侧菜单找到 Pages
echo   4. Source 选择 "Deploy from a branch"
echo   5. Branch 选 "main"，文件夹选 "/ (root)"
echo   6. 点 Save
echo.
echo   等待 1-2 分钟，你的网站就会上线：
echo   https://你的用户名.github.io/仓库名/
echo.
echo ============================================================
echo.
pause
