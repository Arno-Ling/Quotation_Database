#!/bin/bash

# 模具零件数据库查询系统 - Docker启动脚本

set -e

echo "=========================================="
echo "模具零件数据库查询系统 - Docker部署"
echo "=========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker未安装"
    echo "请先安装Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: Docker Compose未安装"
    echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✓ Docker已安装"
echo "✓ Docker Compose已安装"
echo ""

# 检查.env文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  警告: .env文件不存在"
    echo "正在从.env.example创建.env文件..."
    cp .env.example .env
    echo "✓ .env文件已创建"
    echo ""
    echo "⚠️  请编辑.env文件，设置正确的DATABASE_PATH"
    echo "   编辑命令: nano .env 或 vim .env"
    echo ""
    read -p "是否现在编辑.env文件? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    else
        echo "请手动编辑.env文件后再次运行此脚本"
        exit 0
    fi
fi

# 读取DATABASE_PATH
source .env

# 验证DATABASE_PATH是否配置
if [ -z "$DATABASE_PATH" ]; then
    echo "❌ 错误: DATABASE_PATH未配置"
    echo "请编辑.env文件，设置DATABASE_PATH变量"
    exit 1
fi

echo "✓ 数据库路径: $DATABASE_PATH"

# 验证数据库目录是否存在
if [ ! -d "$DATABASE_PATH" ]; then
    echo "❌ 错误: 数据库目录不存在: $DATABASE_PATH"
    echo "请确保DATABASE_PATH指向正确的目录"
    exit 1
fi

echo "✓ 数据库目录存在"
echo ""

# 询问是否重新构建
read -p "是否重新构建镜像? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    BUILD_FLAG="--build"
else
    BUILD_FLAG=""
fi

echo ""
echo "正在启动服务..."
echo ""

# 启动服务
docker-compose up -d $BUILD_FLAG

echo ""
echo "=========================================="
echo "✓ 服务启动成功！"
echo "=========================================="
echo ""
echo "访问地址:"
echo "  前端界面: http://localhost"
echo "  后端API:  http://localhost:8000"
echo "  API文档:  http://localhost:8000/api/docs"
echo ""
echo "常用命令:"
echo "  查看状态: docker-compose ps"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose stop"
echo "  重启服务: docker-compose restart"
echo ""
echo "详细文档: DOCKER_DEPLOYMENT.md"
echo "=========================================="
