#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试API功能的简单脚本
"""

import requests
import json

def test_api():
    """测试API功能"""
    base_url = "http://localhost:8080"
    
    print("🧪 测试中国旅游城市随机推荐API")
    print("=" * 60)
    
    # 测试1: 基本功能
    print("📋 测试1: 基本随机推荐功能")
    test_basic_api(base_url)
    
    print("\n" + "=" * 60)
    
    # 测试2: 省份筛选功能
    print("📋 测试2: 省份筛选功能")
    test_province_filter_api(base_url)
    
    print("\n" + "=" * 60)
    
    # 测试3: 同省城市控制功能
    print("📋 测试3: 同省城市控制功能")
    test_same_province_control_api(base_url)

def test_basic_api(base_url):
    """测试基本API功能"""
    try:
        response = requests.get(f"{base_url}/api/random-cities?count=5")
        if response.status_code == 200:
            data = response.json()
            print("✅ 基本API测试成功！")
            print(f"📊 返回了 {data['count']} 个城市")
            print(f"📈 总共有 {data['total']} 个城市可供选择")
            print("\n🏛️ 推荐的城市：")
            for i, city in enumerate(data['cities'], 1):
                print(f"{i}. {city['name']} ({city['province']}, {city['region']})")
                print(f"   主要玩法: {', '.join(city['activities'][:3])}...")
        else:
            print(f"❌ 基本API测试失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 基本API测试错误: {e}")

def test_province_filter_api(base_url):
    """测试省份筛选功能"""
    try:
        # 测试选择特定省份
        provinces = ["北京", "上海", "广东"]
        response = requests.get(f"{base_url}/api/random-cities?count=3&provinces={'&provinces='.join(provinces)}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 省份筛选API测试成功！")
            print(f"📊 筛选省份: {', '.join(provinces)}")
            print(f"📈 筛选后城市总数: {data['filtered_total']}")
            print("\n🏛️ 推荐的城市：")
            for i, city in enumerate(data['cities'], 1):
                print(f"{i}. {city['name']} ({city['province']}, {city['region']})")
        else:
            print(f"❌ 省份筛选API测试失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 省份筛选API测试错误: {e}")

def test_same_province_control_api(base_url):
    """测试同省城市控制功能"""
    try:
        # 测试避免同省多个城市
        response = requests.get(f"{base_url}/api/random-cities?count=5&same_province=prevent")
        if response.status_code == 200:
            data = response.json()
            print("✅ 同省城市控制API测试成功！")
            print(f"📊 同省城市模式: {data['same_province_mode']}")
            print(f"📈 返回了 {data['count']} 个城市")
            
            # 检查是否来自不同省份
            provinces = [city['province'] for city in data['cities']]
            unique_provinces = set(provinces)
            print(f"📋 涉及省份数量: {len(unique_provinces)}")
            print(f"📋 省份列表: {', '.join(unique_provinces)}")
            
            print("\n🏛️ 推荐的城市：")
            for i, city in enumerate(data['cities'], 1):
                print(f"{i}. {city['name']} ({city['province']}, {city['region']})")
        else:
            print(f"❌ 同省城市控制API测试失败，状态码: {response.status_code}")
    except Exception as e:
        print(f"❌ 同省城市控制API测试错误: {e}")

if __name__ == "__main__":
    test_api()
