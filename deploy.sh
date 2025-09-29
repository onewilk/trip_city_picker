#!/bin/bash

# 部署脚本
echo "🚀 开始部署中国旅游城市推荐工具..."

# 检查必要文件
echo "📋 检查部署文件..."
required_files=("server.py" "index.html" "cities_data.json" "requirements.txt")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ 缺少必要文件: $file"
        exit 1
    fi
done

echo "✅ 所有必要文件检查完成"

# 更新省份数据
echo "🔄 更新省份数据..."
if [ -f "extract_provinces.py" ]; then
    python3 extract_provinces.py
    if [ $? -eq 0 ]; then
        echo "✅ 省份数据更新完成"
    else
        echo "⚠️  省份数据更新失败，但继续部署"
    fi
else
    echo "⚠️  未找到 extract_provinces.py，跳过省份数据更新"
fi

# 创建部署包
echo "📦 创建部署包..."
mkdir -p deploy
cp server.py index.html cities_data.json requirements.txt Procfile railway.json deploy/

# 如果省份数据文件存在，也复制到部署目录
if [ -f "provinces_data.json" ]; then
    cp provinces_data.json deploy/
    echo "✅ 已包含省份数据文件"
fi

echo "✅ 部署包创建完成"
echo "📁 部署文件位于 deploy/ 目录"

echo ""
echo "🎯 下一步操作："
echo "1. 将 deploy/ 目录中的文件上传到 GitHub 仓库"
echo "2. 在 Railway 或 Render 中连接该仓库进行部署"
echo "3. 获取部署URL后，修改前端代码中的API地址"
echo ""
echo "📖 详细说明请查看 部署说明.md"
