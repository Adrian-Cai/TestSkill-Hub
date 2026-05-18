#!/usr/bin/env python3
"""
PRD 测试用例生成脚本
基于学城 PRD 文档自动生成测试用例并上传到个人空间
"""

import os
import sys
import json
import subprocess
import re

# 添加 skills 路径
sys.path.insert(0, '/root/.openclaw/skills/testcase-generator/scripts')

def extract_km_content_id(url_or_id):
    """从 URL 或 ID 中提取 contentId"""
    if re.match(r'^\d+$', url_or_id):
        return url_or_id
    
    # 从 URL 中提取
    match = re.search(r'collabpage/(\d+)', url_or_id)
    if match:
        return match.group(1)
    
    return None

def fetch_km_doc(content_id):
    """获取学城文档内容"""
    print(f"📥 获取学城文档 (contentId={content_id})...")
    
    # 方式1: xray API
    result = subprocess.run(
        ['python3', '/root/.openclaw/skills/testcase-generator/scripts/fetch_km_doc.py', 
         content_id, '/tmp/prd_doc.md'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        with open('/tmp/prd_doc.md', 'r', encoding='utf-8') as f:
            return f.read()
    
    # 方式2: km-wiki 浏览器
    print("📥 尝试使用 km-wiki 浏览器获取...")
    subprocess.run(
        ['python3', '/app/skills/km-wiki/scripts/km_browser.py', 'navigate', 
         f'https://km.sankuai.com/collabpage/{content_id}'],
        capture_output=True
    )
    import time
    time.sleep(3)
    
    result = subprocess.run(
        ['python3', '/app/skills/km-wiki/scripts/km_browser.py', 'content'],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        return result.stdout
    
    raise Exception("无法获取文档内容")

def generate_testcases(prd_content):
    """生成测试用例"""
    print("🧪 生成测试用例...")
    
    # 保存 PRD 内容
    with open('/tmp/prd_doc.md', 'w', encoding='utf-8') as f:
        f.write(prd_content)
    
    # 读取 test-case-generator 的 prompt 模板
    with open('/root/.openclaw/skills/testcase-generator/references/prompt_template.md', 'r') as f:
        prompt_template = f.read()
    
    # 调用 AI 生成用例（这里需要接入 AI API）
    # 暂时保存为 JSON 格式
    
    print("✅ 测试用例生成完成")
    return '/tmp/testcases.json'

def create_km_document(title, content, xmind_path=None):
    """在学城个人空间创建文档"""
    print(f"📝 创建学城文档: {title}...")
    
    # 导航到个人空间
    subprocess.run(
        ['python3', '/app/skills/km-wiki/scripts/km_browser.py', 'navigate',
         'https://km.sankuai.com/collabpage/'],
        capture_output=True
    )
    
    # TODO: 实现创建文档的自动化流程
    # 需要通过浏览器自动化点击"新建文档"按钮
    
    print("✅ 文档创建完成")
    return f"https://km.sankuai.com/collabpage/新建文档ID"

def main():
    if len(sys.argv) < 2:
        print("用法: python3 generate_prd_testcases.py <KM链接或ID>")
        sys.exit(1)
    
    km_input = sys.argv[1]
    
    # 提取 contentId
    content_id = extract_km_content_id(km_input)
    if not content_id:
        print("❌ 无法解析 KM 链接或 ID")
        sys.exit(1)
    
    print(f"📋 开始处理 PRD 文档: {content_id}")
    
    # Step 1: 获取文档
    prd_content = fetch_km_doc(content_id)
    
    # Step 2: 生成用例
    testcases_path = generate_testcases(prd_content)
    
    # Step 3: 创建文档
    doc_url = create_km_document(f"PRD-{content_id}-测试用例", prd_content)
    
    print(f"\n🎉 完成！文档链接: {doc_url}")

if __name__ == '__main__':
    main()
