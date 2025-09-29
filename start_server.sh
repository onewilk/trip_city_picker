#!/bin/bash

# 中国旅游城市随机推荐工具启动脚本

echo "🏛️  中国旅游城市随机推荐工具"
echo "=================================="

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python3"
    exit 1
fi

# 检查必要文件
if [ ! -f "cities_data.json" ]; then
    echo "❌ 错误: cities_data.json 文件不存在"
    exit 1
fi

if [ ! -f "index.html" ]; then
    echo "❌ 错误: index.html 文件不存在"
    exit 1
fi

if [ ! -f "server.py" ]; then
    echo "❌ 错误: server.py 文件不存在"
    exit 1
fi

echo "✅ 所有必要文件检查完成"
echo "🚀 正在启动服务器..."
echo ""

# 启动服务器
python3 server.py
