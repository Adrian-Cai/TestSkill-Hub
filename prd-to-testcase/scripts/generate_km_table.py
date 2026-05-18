#!/usr/bin/env python3
"""
将测试用例 JSON 转换为学城测试用例模板格式
支持双文档输入：PRD + 技术文档
参考: https://km.sankuai.com/collabpage/2711140979
"""
import json
import sys
import re

def extract_km_link(text):
    """提取 KM 链接"""
    match = re.search(r'https?://km\.sankuai\.com/collabpage/(\d+)', text)
    if match:
        return match.group(0), match.group(1)
    # 纯数字
    if text.strip().isdigit():
        return f"https://km.sankuai.com/collabpage/{text}", text
    return None, None

def generate_template_html(prd_name, prd_url, json_file, xmind_url=None, tech_doc_url=None):
    """生成学城测试用例模板格式的 HTML"""
    
    # 读取测试用例
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html = f'<h1>{prd_name} 测试用例</h1>\n\n'
    
    # 1. 需求描述
    html += '<h2>1 需求描述</h2>\n'
    html += f'<p>基于 PRD 文档和技术文档生成的测试用例</p>\n\n'
    
    # 2. 相关链接
    html += '<h2>2 相关链接</h2>\n'
    html += '<table border="1" cellpadding="5" cellspacing="0">\n'
    html += '<tr><th>类型</th><th>URL</th><th>备注</th></tr>\n'
    html += f'<tr><td>需求文档(PRD)</td><td><a href="{prd_url}">{prd_url}</a></td><td>产品需求</td></tr>\n'
    if tech_doc_url:
        html += f'<tr><td>技术文档</td><td><a href="{tech_doc_url}">{tech_doc_url}</a></td><td>技术方案</td></tr>\n'
    if xmind_url:
        html += f'<tr><td>XMind思维导图</td><td><a href="{xmind_url}">下载链接</a></td><td>用例脑图</td></tr>\n'
    html += '</table>\n\n'
    
    # 3. 测试策略
    html += '<h2>3 测试策略</h2>\n'
    html += '<h3>3.1 业务范围</h3>\n'
    html += '<p>{}</p>\n\n'.format(prd_name)
    
    html += '<h3>3.2 测试方式</h3>\n'
    html += '<ul>\n'
    html += '<li>功能测试：验证各模块功能是否符合PRD要求</li>\n'
    html += '<li>接口测试：验证API参数、返回值是否符合技术文档定义</li>\n'
    html += '<li>UI测试：验证页面展示、交互是否符合预期</li>\n'
    html += '<li>兼容性测试：验证不同版本、不同设备表现</li>\n'
    html += '</ul>\n\n'
    
    html += '<h3>3.3 测试周期</h3>\n'
    html += '<p>预计测试周期：X天</p>\n\n'
    
    html += '<h3>3.4 自动化用例</h3>\n'
    html += '<p>待补充自动化用例脚本</p>\n\n'
    
    # 4. 冒烟用例
    html += '<h2>4 冒烟用例</h2>\n'
    html += '<table border="1" cellpadding="5" cellspacing="0">\n'
    html += '<tr><th>场景</th><th>用例名</th><th>期望结果</th><th>测试结果</th><th>状态</th></tr>\n'
    
    p0_count = 0
    for module in data['modules']:
        for scenario in module['scenarios']:
            for case in scenario['cases']:
                if case.get('priority') == 'P0' and p0_count < 10:
                    html += '<tr>'
                    html += '<td>{}</td>'.format(scenario['name'])
                    html += '<td>{}</td>'.format(case.get('title', ''))
                    html += '<td>{}</td>'.format(case.get('expected', '').replace('\n', '<br>'))
                    html += '<td></td>'
                    html += '<td>待测试</td>'
                    html += '</tr>\n'
                    p0_count += 1
    
    html += '</table>\n\n'
    
    # 5. 测试用例
    html += '<h2>5 测试用例</h2>\n'
    html += '<table border="1" cellpadding="5" cellspacing="0">\n'
    html += '<tr><th>场景</th><th>用例名</th><th>前置条件</th><th>测试步骤</th><th>期望结果</th><th>优先级</th><th>测试结果</th><th>状态</th><th>备注</th></tr>\n'
    
    for module in data['modules']:
        for scenario in module['scenarios']:
            for case in scenario['cases']:
                html += '<tr>'
                html += '<td>{}</td>'.format(scenario['name'])
                html += '<td>{}</td>'.format(case.get('title', ''))
                html += '<td>{}</td>'.format(case.get('precondition', '').replace('\n', '<br>'))
                html += '<td>{}</td>'.format(case.get('steps', '').replace('\n', '<br>'))
                html += '<td>{}</td>'.format(case.get('expected', '').replace('\n', '<br>'))
                html += '<td>{}</td>'.format(case.get('priority', ''))
                html += '<td></td>'
                html += '<td>待测试</td>'
                html += '<td>{}</td>'.format(case.get('method', ''))
                html += '</tr>\n'
    
    html += '</table>\n\n'
    
    # 6. 测试日报
    html += '<h2>6 测试日报</h2>\n'
    html += '<table border="1" cellpadding="5" cellspacing="0">\n'
    html += '<tr><th>日期</th><th>测试内容</th><th>发现bug</th><th>备注</th></tr>\n'
    html += '<tr><td></td><td></td><td></td><td></td></tr>\n'
    html += '</table>\n\n'
    
    # 7. 相关问题汇总
    html += '<h2>7 相关问题汇总</h2>\n'
    html += '<table border="1" cellpadding="5" cellspacing="0">\n'
    html += '<tr><th>问题描述</th><th>严重程度</th><th>状态</th><th>备注</th></tr>\n'
    html += '<tr><td></td><td></td><td></td><td></td></tr>\n'
    html += '</table>\n\n'
    
    return html

def parse_input(input_text):
    """解析输入文本，提取文档链接"""
    # 查找所有 KM 链接
    links = re.findall(r'https?://km\.sankuai\.com/collabpage/\d+', input_text)
    
    if len(links) >= 2:
        return links[0], links[1]  # PRD, 技术文档
    elif len(links) == 1:
        return links[0], None
    else:
        # 尝试提取纯数字
        nums = re.findall(r'\b\d+\b', input_text)
        if nums:
            prd_id = nums[0]
            return f"https://km.sankuai.com/collabpage/{prd_id}", None
    return None, None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python3 generate_km_table.py <PRD名称> <输入文本> <testcases.json> [XMind链接]")
        print("输入文本可以是: PRD链接 或 PRD链接+技术文档链接")
        sys.exit(1)
    
    prd_name = sys.argv[1]
    input_text = sys.argv[2]
    json_file = sys.argv[3]
    xmind_url = sys.argv[4] if len(sys.argv) > 4 else None
    
    prd_url, tech_doc_url = parse_input(input_text)
    
    if not prd_url:
        print("错误：未找到有效的 KM 文档链接")
        sys.exit(1)
    
    html = generate_template_html(prd_name, prd_url, json_file, xmind_url, tech_doc_url)
    
    output_file = '/tmp/testcases_template.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"模板已生成: {output_file}")
    if tech_doc_url:
        print(f"技术文档: {tech_doc_url}")
