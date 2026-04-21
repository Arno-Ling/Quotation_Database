@echo off
REM 模具零件数据库查询系统 - Docker启动脚本 (Windows)

echo ==========================================
echo 模具零件数据库查询系统 - Docker部署
echo ==========================================
echo.

REM 检查Docker是否安装
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: Docker未安装
    echo 请先安装Docker Desktop: https://docs.docker.com/desktop/install/windows-install/
    pause
    exit /b 1
)

REM 检查Docker Compose是否安装
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: Docker Compose未安装
    echo Docker Desktop应该已包含Docker Compose
    pause
    exit /b 1
)

echo ✓ Docker已安装
echo ✓ Docker Compose已安装
echo.

REM 检查.env文件是否存在
if not exist .env (
    echo ⚠️  警告: .env文件不存在
    echo 正在从.env.example创建.env文件...
    copy .env.example .env >nul
    echo ✓ .env文件已创建
    echo.
    echo ⚠️  请编辑.env文件，设置正确的DATABASE_PATH
    echo    编辑命令: notepad .env
    echo.
    set /p EDIT="是否现在编辑.env文件? (y/n) "
    if /i "%EDIT%"=="y" (
        notepad .env
    ) else (
        echo 请手动编辑.env文件后再次运行此脚本
        pause
        exit /b 0
    )
)

REM 读取DATABASE_PATH（简化版本，仅显示提示）
echo ✓ 配置文件已加载
echo.

REM 询问是否重新构建
set /p REBUILD="是否重新构建镜像? (y/n) "
if /i "%REBUILD%"=="y" (
    set BUILD_FLAG=--build
) else (
    set BUILD_FLAG=
)

echo.
echo 正在启动服务...
echo.

REM 启动服务
docker-compose up -d %BUILD_FLAG%

if errorlevel 1 (
    echo.
    echo ❌ 启动失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ==========================================
echo ✓ 服务启动成功！
echo ==========================================
echo.
echo 访问地址:
echo   前端界面: http://localhost
echo   后端API:  http://localhost:8000
echo   API文档:  http://localhost:8000/api/docs
echo.
echo 常用命令:
echo   查看状态: docker-compose ps
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose stop
echo   重启服务: docker-compose restart
echo.
echo 详细文档: DOCKER_DEPLOYMENT.md
echo ==========================================
echo.
pause
