@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
echo ==============================================
echo       递归批量转换为渐进式图片（修复老版本）
echo ==============================================
echo.

:: 递归 JPG（老版本通用）
for /r %%i in (*.jpg *.jpeg) do (
    echo 处理：%%~fi
    convert "%%i" -interlace Plane "%%i"
)

:: 递归 PNG（老版本用 line，去掉 Adam7）
for /r %%i in (*.png) do (
    echo 处理：%%~fi
    convert "%%i" -interlace Line "%%i"
)

echo.
echo ==============================================
echo ✅ 全部转换完成！所有文件已直接转为渐进式
echo ==============================================
pause
exit