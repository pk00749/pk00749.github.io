#!/usr/bin/env python3
"""
微信公众号文章HTML转换工具
将Markdown或纯文本转换为微信公众号兼容的HTML
"""

import re
import sys
import html

def escape_html(text):
    """转义HTML特殊字符"""
    return html.escape(text)

def markdown_to_wechat_html(markdown_text, cover_image=None, author=""):
    """
    将Markdown转换为微信公众号兼容的HTML
    
    Args:
        markdown_text: Markdown格式的文章内容
        cover_image: 封面图片URL（可选）
        author: 作者名称（可选）
    
    Returns:
        微信公众号兼容的HTML字符串
    """
    lines = markdown_text.strip().split('\n')
    html_content = []
    in_code_block = False
    in_list = False
    in_ordered_list = False
    
    for line in lines:
        line = line.rstrip()
        
        # 代码块
        if line.startswith('```'):
            if in_code_block:
                html_content.append('</code></pre>')
                in_code_block = False
            else:
                lang = line[3:].strip() if len(line) > 3 else ''
                html_content.append(f'<pre><code class="language-{lang}">')
                in_code_block = True
            continue
        
        if in_code_block:
            html_content.append(escape_html(line))
            continue
        
        # 跳过空行
        if not line.strip():
            continue
        
        # 标题处理
        if line.startswith('### '):
            html_content.append(f'<h3>{escape_html(line[4:])}</h3>')
        elif line.startswith('## '):
            html_content.append(f'<h2>{escape_html(line[3:])}</h2>')
        elif line.startswith('# '):
            html_content.append(f'<h1>{escape_html(line[2:])}</h1>')
        
        # 分割线
        elif line in ['---', '***', '___']:
            html_content.append('<hr/>')
        
        # 无序列表
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list or in_ordered_list:
                if in_ordered_list:
                    html_content.append('</ol>')
                html_content.append('<ul>')
                in_list = True
                in_ordered_list = False
            html_content.append(f'<li>{escape_html(line[2:])}</li>')
        
        # 有序列表
        elif re.match(r'^\d+\.\s', line):
            if not in_list or not in_ordered_list:
                if in_list and not in_ordered_list:
                    html_content.append('</ul>')
                html_content.append('<ol>')
                in_list = True
                in_ordered_list = True
            cleaned_line = re.sub(r"^\d+\.\s", "", line)
            html_content.append(f'<li>{cleaned_line}</li>')
        
        # 引用
        elif line.startswith('> '):
            html_content.append(f'<blockquote>{escape_html(line[2:])}</blockquote>')
        
        # 图片
        elif line.startswith('!['):
            match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            if match:
                alt_text, img_url = match.groups()
                html_content.append(f'<p><img src="{img_url}" alt="{alt_text}"/></p>')
        
        # 链接
        elif '[text]' in line and '(url)' in line:
            match = re.match(r'\[(.*?)\]\((.*?)\)', line)
            if match:
                link_text, link_url = match.groups()
                html_content.append(f'<p><a href="{link_url}">{escape_html(link_text)}</a></p>')
        
        # 普通段落（处理加粗、斜体等）
        else:
            if in_list:
                if in_ordered_list:
                    html_content.append('</ol>')
                else:
                    html_content.append('</ul>')
                in_list = False
                in_ordered_list = False
            
            # 处理行内格式
            formatted = escape_html(line)
            formatted = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', formatted)
            formatted = re.sub(r'__(.+?)__', r'<strong>\1</strong>', formatted)
            formatted = re.sub(r'\*(.+?)\*', r'<em>\1</em>', formatted)
            formatted = re.sub(r'_(.+?)_', r'<em>\1</em>', formatted)
            formatted = re.sub(r'~~(.+?)~~', r'<s>\1</s>', formatted)
            formatted = re.sub(r'`(.+?)`', r'<code>\1</code>', formatted)
            
            html_content.append(f'<p>{formatted}</p>')
    
    # 关闭列表
    if in_list:
        if in_ordered_list:
            html_content.append('</ol>')
        else:
            html_content.append('</ul>')
    
    # 构建完整HTML
    result = ''.join(html_content)
    
    # 添加作者信息
    if author:
        result = f'<p style="text-align:right;color:#999;">作者：{escape_html(author)}</p>' + result
    
    return result


def text_to_wechat_html(text, cover_image=None, author=""):
    """
    将纯文本转换为微信公众号兼容的HTML
    
    Args:
        text: 纯文本内容
        cover_image: 封面图片URL（可选）
        author: 作者名称（可选）
    
    Returns:
        微信公众号兼容的HTML字符串
    """
    # 简单的文本处理：识别标题和段落
    lines = text.strip().split('\n')
    html_content = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # 如果是全大写的行，作为标题
        if line.isupper() and len(line) > 3:
            html_content.append(f'<h2>{escape_html(line)}</h2>')
        # 以冒号结尾的行，可能是小标题
        elif line.endswith(':') and len(line) < 50:
            html_content.append(f'<h3>{escape_html(line)}</h3>')
        # 普通段落
        else:
            html_content.append(f'<p>{escape_html(line)}</p>')
    
    if author:
        html_content.insert(0, f'<p style="text-align:right;color:#999;">作者：{escape_html(author)}</p>')
    
    return ''.join(html_content)


def main():
    if len(sys.argv) < 3:
        print("用法: md_to_wechat.py <输入文件> <输出文件> [封面图片URL] [作者]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    cover_image = sys.argv[3] if len(sys.argv) > 3 else None
    author = sys.argv[4] if len(sys.argv) > 4 else ""
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检测内容类型并转换
    if content.strip().startswith('#') or '```' in content or '**' in content:
        html_result = markdown_to_wechat_html(content, cover_image, author)
    else:
        html_result = text_to_wechat_html(content, cover_image, author)
    
    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_result)
    
    print(f"转换完成，已保存到: {output_file}")
    
    if cover_image:
        print(f"封面图片: {cover_image}")


if __name__ == '__main__':
    main()
