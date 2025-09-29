#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从城市数据中提取省份信息
"""

import json
import os

def extract_provinces():
    """从城市数据中提取省份信息"""
    
    # 读取城市数据
    try:
        with open('cities_data.json', 'r', encoding='utf-8') as f:
            cities_data = json.load(f)
    except FileNotFoundError:
        print("错误: cities_data.json 文件不存在")
        return
    except json.JSONDecodeError:
        print("错误: cities_data.json 文件格式错误")
        return
    
    # 提取省份信息
    provinces = set()
    for city in cities_data:
        if 'province' in city:
            provinces.add(city['province'])
    
    # 排序并转换为列表
    provinces_list = sorted(list(provinces))
    
    # 保存省份数据
    try:
        with open('provinces_data.json', 'w', encoding='utf-8') as f:
            json.dump(provinces_list, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 成功提取 {len(provinces_list)} 个省份")
        print(f"📁 省份数据已保存到 provinces_data.json")
        print(f"📋 省份列表: {', '.join(provinces_list[:10])}{'...' if len(provinces_list) > 10 else ''}")
        
    except Exception as e:
        print(f"❌ 保存省份数据失败: {e}")

if __name__ == "__main__":
    extract_provinces()
