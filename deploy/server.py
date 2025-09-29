#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国旅游城市随机推荐工具 - HTTP服务器
支持局域网访问的简单Web服务器
"""

import http.server
import socketserver
import json
import os
import socket
import webbrowser
from urllib.parse import urlparse, parse_qs
import random

class CityRecommendationHandler(http.server.SimpleHTTPRequestHandler):
    """自定义HTTP请求处理器"""
    
    def __init__(self, *args, **kwargs):
        # 加载城市数据
        self.cities_data = self.load_cities_data()
        super().__init__(*args, **kwargs)
    
    def load_cities_data(self):
        """加载城市数据"""
        try:
            with open('cities_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("警告: cities_data.json 文件未找到")
            return []
        except json.JSONDecodeError:
            print("警告: cities_data.json 文件格式错误")
            return []
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        
        # API接口：获取随机城市
        if parsed_path.path == '/api/random-cities':
            self.handle_random_cities_api(parsed_path.query)
        else:
            # 静态文件服务
            super().do_GET()
    
    def handle_random_cities_api(self, query_string):
        """处理随机城市API请求"""
        try:
            # 解析查询参数
            params = parse_qs(query_string)
            count = int(params.get('count', ['5'])[0])
            provinces = params.get('provinces', [])
            same_province_mode = params.get('same_province', ['allow'])[0]
            
            # 验证参数
            if count < 1 or count > 100:
                self.send_error_response(400, "城市数量必须在1-100之间")
                return
            
            # 根据省份筛选城市
            filtered_cities = self.cities_data
            if provinces:
                filtered_cities = [city for city in self.cities_data if city['province'] in provinces]
            
            if not filtered_cities:
                self.send_error_response(400, "所选省份中没有城市数据")
                return
            
            if count > len(filtered_cities):
                self.send_error_response(400, f"所选省份中最多只能选择 {len(filtered_cities)} 个城市")
                return
            
            # 根据同省城市模式选择城市
            if same_province_mode == 'prevent':
                random_cities = self.get_random_cities_from_different_provinces(filtered_cities, count)
            else:
                random_cities = random.sample(filtered_cities, count)
            
            # 返回JSON响应
            response_data = {
                'success': True,
                'count': count,
                'cities': random_cities,
                'total': len(self.cities_data),
                'filtered_total': len(filtered_cities),
                'provinces': provinces,
                'same_province_mode': same_province_mode
            }
            
            self.send_json_response(response_data)
            
        except ValueError:
            self.send_error_response(400, "无效的参数")
        except Exception as e:
            self.send_error_response(500, f"服务器错误: {str(e)}")
    
    def get_random_cities_from_different_provinces(self, cities, count):
        """从不同省份随机选择城市"""
        province_groups = {}
        
        # 按省份分组
        for city in cities:
            province = city['province']
            if province not in province_groups:
                province_groups[province] = []
            province_groups[province].append(city)
        
        provinces = list(province_groups.keys())
        result = []
        
        # 如果请求的城市数量小于等于省份数量，每个省份选一个
        if count <= len(provinces):
            random.shuffle(provinces)
            for i in range(count):
                province = provinces[i]
                random_city = random.choice(province_groups[province])
                result.append(random_city)
        else:
            # 如果请求的城市数量大于省份数量，先每个省份选一个，然后随机补充
            for province in provinces:
                random_city = random.choice(province_groups[province])
                result.append(random_city)
            
            # 随机补充剩余的城市
            remaining_count = count - len(provinces)
            all_remaining_cities = [city for city in cities if city not in result]
            if all_remaining_cities:
                additional_cities = random.sample(all_remaining_cities, 
                                                min(remaining_count, len(all_remaining_cities)))
                result.extend(additional_cities)
        
        return result
    
    def send_json_response(self, data):
        """发送JSON响应"""
        response_data = json.dumps(data, ensure_ascii=False, indent=2)
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(response_data.encode('utf-8'))
    
    def send_error_response(self, code, message):
        """发送错误响应"""
        error_data = {
            'success': False,
            'error': message,
            'code': code
        }
        
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response_data = json.dumps(error_data, ensure_ascii=False)
        self.wfile.write(response_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志格式"""
        print(f"[{self.date_time_string()}] {format % args}")

def get_local_ip():
    """获取本机IP地址"""
    try:
        # 创建一个socket连接来获取本机IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """主函数"""
    PORT = 8080
    
    # 确保在正确的目录中运行
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 检查必要文件是否存在
    if not os.path.exists('cities_data.json'):
        print("错误: cities_data.json 文件不存在")
        return
    
    if not os.path.exists('index.html'):
        print("错误: index.html 文件不存在")
        return
    
    # 创建服务器
    with socketserver.TCPServer(("", PORT), CityRecommendationHandler) as httpd:
        local_ip = get_local_ip()
        
        print("=" * 60)
        print("🏛️  中国旅游城市随机推荐工具")
        print("=" * 60)
        print(f"📡 服务器已启动")
        print(f"🌐 本地访问: http://localhost:{PORT}")
        print(f"🌍 局域网访问: http://{local_ip}:{PORT}")
        
        # 检查是否在云环境中运行
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER'):
            print(f"☁️  云部署环境: 已检测到")
            print(f"🌐 公网访问: https://your-app.railway.app (请替换为实际域名)")
        
        print("=" * 60)
        print("📋 功能说明:")
        print("   • 随机推荐1-100个中国旅游城市")
        print("   • 覆盖全国各省市，避免过度集中")
        print("   • 每个城市包含详细的主要玩法")
        print("   • 支持统计信息显示")
        print("=" * 60)
        print("💡 使用说明:")
        print("   1. 在浏览器中打开上述地址")
        print("   2. 选择想要的城市数量")
        print("   3. 点击'随机推荐'按钮")
        print("   4. 查看推荐结果")
        print("=" * 60)
        print("🛑 按 Ctrl+C 停止服务器")
        print("=" * 60)
        
        # 自动打开浏览器
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("🚀 已自动打开浏览器")
        except:
            print("⚠️  无法自动打开浏览器，请手动访问上述地址")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 服务器已停止")
            print("感谢使用！")

if __name__ == "__main__":
    main()
