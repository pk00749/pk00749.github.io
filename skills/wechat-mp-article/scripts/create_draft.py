#!/usr/bin/env python3
"""
微信公众号草稿创建工具
调用微信公众平台API创建草稿
"""

import json
import os
import sys
import requests
import time

# 微信公众号API配置
API_BASE_URL = "https://api.weixin.qq.com"

# 从环境变量或配置文件获取凭证
def get_credentials():
    """获取公众号凭证"""
    # 优先从环境变量获取
    app_id = os.environ.get('WECHAT_APP_ID')
    app_secret = os.environ.get('WECHAT_APP_SECRET')
    
    if app_id and app_secret:
        return app_id, app_secret
    
    # 尝试从配置文件读取
    config_file = os.path.expanduser('~/.wechat_mp_config')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get('app_id'), config.get('app_secret')
    
    return None, None


def get_access_token(app_id, app_secret):
    """
    获取微信公众平台access_token
    
    Args:
        app_id: 公众号AppID
        app_secret: 公众号AppSecret
    
    Returns:
        access_token字符串，失败返回None
    """
    url = f"{API_BASE_URL}/cgi-bin/token"
    params = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': app_secret
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        if 'access_token' in result:
            print(f"获取access_token成功")
            return result['access_token']
        else:
            print(f"获取access_token失败: {result.get('errmsg', '未知错误')}")
            return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def upload_thumb_media(access_token, thumb_url):
    """
    上传封面图片（永久素材）
    
    Args:
        access_token: 微信access_token
        thumb_url: 封面图片URL
    
    Returns:
        media_id，失败返回None
    """
    # 由于图片是URL，需要先下载再上传
    try:
        # 下载图片
        img_response = requests.get(thumb_url, timeout=30)
        if img_response.status_code != 200:
            print(f"下载图片失败: {thumb_url}")
            return None
        
        # 获取图片内容
        img_content = img_response.content
        img_size = len(img_content)
        
        # 检查文件大小（微信限制2MB）
        if img_size > 2 * 1024 * 1024:
            print(f"图片太大: {img_size} bytes，最大支持2MB")
            return None
        
        # 上传图片
        url = f"{API_BASE_URL}/cgi-bin/media/uploadimg"
        params = {'access_token': access_token}
        
        files = {'media': ('cover.jpg', img_content, 'image/jpeg')}
        response = requests.post(url, files=files, params=params, timeout=30)
        result = response.json()
        
        if 'media_id' in result:
            print(f"封面上传成功，media_id: {result['media_id']}")
            return result['media_id']
        else:
            print(f"封面上传失败: {result.get('errmsg', '未知错误')}")
            return None
            
    except Exception as e:
        print(f"上传封面失败: {e}")
        return None


def add_draft(access_token, articles):
    """
    创建草稿
    
    Args:
        access_token: 微信access_token
        articles: 文章列表，每篇文章包含title, author, content, digest, content_source_url等
    
    Returns:
        成功返回draft_id，失败返回None
    """
    url = f"{API_BASE_URL}/cgi-bin/draft/add"
    params = {'access_token': access_token}
    
    data = {
        'articles': articles
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=30)
        result = response.json()
        
        if 'draft_id' in result:
            print(f"草稿创建成功，draft_id: {result['draft_id']}")
            return result['draft_id']
        else:
            print(f"草稿创建失败: {result.get('errmsg', '未知错误')}")
            return None
    except Exception as e:
        print(f"创建草稿请求失败: {e}")
        return None


def create_wechat_draft(html_file, title, author="", cover_url="", digest=""):
    """
    创建微信公众号草稿的完整流程
    
    Args:
        html_file: HTML内容文件路径
        title: 文章标题
        author: 作者（可选）
        cover_url: 封面图片URL（可选）
        digest: 文章摘要（可选）
    
    Returns:
        draft_id或None
    """
    # 获取凭证
    app_id, app_secret = get_credentials()
    
    if not app_id or not app_secret:
        print("错误: 请配置微信公众号AppID和AppSecret")
        print("方式1: 设置环境变量 WECHAT_APP_ID 和 WECHAT_APP_SECRET")
        print("方式2: 创建 ~/.wechat_mp_config 文件，格式如下：")
        print('{"app_id": "your_app_id", "app_secret": "your_app_secret"}')
        return None
    
    print(f"使用公众号AppID: {app_id}")
    
    # 获取access_token
    access_token = get_access_token(app_id, app_secret)
    if not access_token:
        return None
    
    # 读取HTML内容
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 准备文章数据
    article = {
        'title': title,
        'author': author,
        'content': content,
        'content_source_url': '',
        'digest': digest or title[:120],  # 摘要默认取标题前120字
    }
    
    # 如果提供了封面图片，先上传
    if cover_url:
        media_id = upload_thumb_media(access_token, cover_url)
        if media_id:
            article['thumb_media_id'] = media_id
    
    # 创建草稿
    draft_id = add_draft(access_token, [article])
    
    return draft_id


def main():
    if len(sys.argv) < 3:
        print("用法: create_draft.py <html文件> <标题> [作者] [封面图片URL] [摘要]")
        print("")
        print("示例:")
        print("  create_draft.py article.html '我的文章' '张三' 'https://example.com/cover.jpg'")
        sys.exit(1)
    
    html_file = sys.argv[1]
    title = sys.argv[2]
    author = sys.argv[3] if len(sys.argv) > 3 else ""
    cover_url = sys.argv[4] if len(sys.argv) > 4 else ""
    digest = sys.argv[5] if len(sys.argv) > 5 else ""
    
    # 检查文件是否存在
    if not os.path.exists(html_file):
        print(f"错误: 文件不存在: {html_file}")
        sys.exit(1)
    
    print(f"开始创建草稿...")
    print(f"标题: {title}")
    if author:
        print(f"作者: {author}")
    if cover_url:
        print(f"封面: {cover_url}")
    
    draft_id = create_wechat_draft(html_file, title, author, cover_url, digest)
    
    if draft_id:
        print(f"\n✅ 草稿创建成功！")
        print(f"草稿ID: {draft_id}")
        print(f"你可以在微信公众号后台编辑和发布这篇草稿")
    else:
        print(f"\n❌ 草稿创建失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
