# notifier.py
import requests
import json
import time
import html
from config import PUSHPLUS_TOKEN, SERVERCHAN_KEY, WECHAT_APPID, WECHAT_APPSECRET, WECHAT_TEMPLATE_ID, WECHAT_USER_OPENID, WXPUSHER_APP_TOKEN, WXPUSHER_USER_UID

def send_pushplus(subject, content):
    """
    Send via PushPlus
    """
    if not PUSHPLUS_TOKEN:
        print("PushPlus Token not configured. Skipping.")
        return False
        
    url = "http://www.pushplus.plus/send"
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": subject,
        "content": content,
        "template": "html"
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        if result.get("code") == 200:
            print("PushPlus send success")
            return True
        else:
            print(f"PushPlus failed: {result}")
            return False
    except Exception as e:
        print(f"PushPlus Error: {e}")
        return False

def send_serverchan(subject, content):
    """
    Send via ServerChan (Turbo)
    """
    if not SERVERCHAN_KEY:
        print("ServerChan Key not configured. Skipping.")
        return False
        
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
    data = {
        "title": subject,
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        if result.get("code") == 0:
            print("ServerChan send success")
            return True
        else:
            print(f"ServerChan failed: {result}")
            return False
    except Exception as e:
        print(f"ServerChan Error: {e}")
        return False

def send_wechat_test(subject, content):
    """
    Send via WeChat Test Account using template message.
    """
    if not all([WECHAT_APPID, WECHAT_APPSECRET, WECHAT_TEMPLATE_ID, WECHAT_USER_OPENID]):
        print("WeChat Test Account not fully configured. Skipping.")
        return False
    
    try:
        # 1. Get access token
        token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={WECHAT_APPID}&secret={WECHAT_APPSECRET}"
        token_response = requests.get(token_url, timeout=10)
        token_data = token_response.json()
        
        if 'access_token' not in token_data:
            print(f"WeChat token error: {token_data}")
            return False
        
        access_token = token_data['access_token']
        
        # 2. Prepare template data with more detailed information
        import re
        from bs4 import BeautifulSoup
        
        # 解析HTML获取详细信息
        soup = BeautifulSoup(content, 'html.parser')
        platform_divs = soup.find_all('div', style=re.compile(r'background: #f8f9fa'))
        platform_count = len(platform_divs)
        
        # 提取各平台热点，提供更详细的信息
        hot_items = []
        successful_platforms = 0
        platform_details = []
        
        for div in platform_divs:
            h2 = div.find('h2')
            if not h2:
                continue
                
            platform_name = h2.get_text(strip=True).replace('🔥', '').strip()
            items = div.find_all('li')
            
            # 检查是否有真实数据
            has_real_data = False
            platform_hot_items = []
            
            for item in items[:5]:  # 每个平台最多检查5条
                text = item.get_text(strip=True)
                if not text or len(text) < 4:
                    continue
                    
                # 过滤错误信息
                error_keywords = ['Error', '错误', '暂无数据', 'Config Required', 'Could not parse', 'Scraper']
                if any(keyword in text for keyword in error_keywords):
                    continue
                
                # 提取排名、标题和热度
                match = re.match(r'(\d+)\s*(.+?)(?:\s+(\d+[万MkK]?))?$', text)
                if match:
                    rank = match.group(1)
                    title = match.group(2).strip()
                    hot_value = match.group(3) if match.group(3) else ""
                    
                    if title and len(title) > 2:
                        has_real_data = True
                        # 格式化：排名. 标题 (热度)
                        formatted = f"{rank}. {title}"
                        if hot_value:
                            formatted += f" ({hot_value})"
                        platform_hot_items.append(formatted)
            
            # 记录有数据的平台
            if has_real_data and platform_hot_items:
                successful_platforms += 1
                platform_details.append({
                    'name': platform_name,
                    'items': platform_hot_items[:3]  # 每个平台最多3条
                })
                
                # 为模板摘要准备数据（前3个平台，每个平台前2条）
                if successful_platforms <= 3:
                    for item in platform_hot_items[:2]:
                        # 简化显示
                        simple_item = re.sub(r'^\d+\.\s*', '', item)
                        if len(simple_item) > 25:
                            simple_item = simple_item[:22] + "..."
                        hot_items.append(f"• {platform_name}: {simple_item}")
        
        # 生成详细的热点摘要
        if hot_items:
            hot_summary = "\n".join(hot_items[:6])  # 最多6条
            if len(hot_items) > 6:
                hot_summary += f"\n...查看更多"
        else:
            hot_summary = "暂无热点数据"
        
        # 生成平台统计信息
        if successful_platforms > 0:
            platform_names = [p['name'] for p in platform_details[:3]]
            platform_info = f"{successful_platforms}个平台有数据"
            if platform_names:
                platform_info += f" ({'、'.join(platform_names)})"
        else:
            platform_info = f"{platform_count}个平台均无数据"
        
        # 3. 生成详细报告并上传到临时服务（这里简化，实际可以上传到服务器或使用云存储）
        # 由于微信模板限制，我们只能提供摘要，详细报告需要其他方式
        
        # 4. Send template message with improved content
        send_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
        
        # 改进的模板数据 - 更友好的排版
        template_data = {
            "touser": WECHAT_USER_OPENID,
            "template_id": WECHAT_TEMPLATE_ID,
            "url": "https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login",  # 如果有公众号文章链接可以替换
            "data": {
                "first": {
                    "value": f"🔥 {subject} 🔥\n────────────",
                    "color": "#e74c3c"
                },
                "keyword1": {
                    "value": time.strftime("%m月%d日 %H:%M"),
                    "color": "#3498db"
                },
                "keyword2": {
                    "value": platform_info,
                    "color": "#2ecc71"
                },
                "keyword3": {
                    "value": hot_summary,
                    "color": "#34495e"
                },
                "remark": {
                    "value": "📱 点击查看完整热点榜单\n🔍 数据来源：各平台公开榜单",
                    "color": "#7f8c8d"
                }
            }
        }
        
        response = requests.post(send_url, json=template_data, timeout=10)
        result = response.json()
        
        if result.get('errcode') == 0:
            print("WeChat Test Account send success")
            
            # 同时输出详细数据到控制台，方便查看
            print("\n=== 详细热点数据 ===")
            for platform in platform_details:
                print(f"\n{platform['name']}:")
                for item in platform['items']:
                    print(f"  {item}")
            print(f"\n总计: {successful_platforms}/{platform_count}个平台有数据")
            
            return True
        else:
            print(f"WeChat Test Account failed: {result}")
            return False
            
    except Exception as e:
        print(f"WeChat Test Account Error: {e}")
        return False

def send_wxpusher(subject, content):
    """
    Send via WxPusher (支持长文本和Markdown)
    """
    if not all([WXPUSHER_APP_TOKEN, WXPUSHER_USER_UID]):
        print("WxPusher not configured. Skipping.")
        return False
    
    try:
        # 将HTML转换为Markdown格式，更适合WxPusher
        import re
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # 提取主要信息生成Markdown
        markdown_content = f"# {subject}\n\n"
        markdown_content += f"**时间**: {time.strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # 提取各平台数据，增加显示数量
        platform_divs = soup.find_all('div', style=re.compile(r'background: #f8f9fa'))
        
        for div in platform_divs[:12]:  # 最多12个平台
            h2 = div.find('h2')
            if not h2:
                continue
                
            platform_name = h2.get_text(strip=True).replace('🔥', '').strip()
            
            # 根据不同平台调整显示数量
            if platform_name in ["Weibo", "微博", "Douyin", "抖音"]:
                items = div.find_all('li')[:15]  # 微博抖音显示15条
            elif platform_name in ["Twitter", "推特"]:
                items = div.find_all('li')[:20]  # 推特显示20条（中文区优先）
            else:
                items = div.find_all('li')[:8]   # 其他平台显示8条
            
            valid_items = []
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 3:
                    # 过滤错误信息
                    if any(keyword in text for keyword in ['Error', '错误', '暂无数据', 'Config Required', 'Could not parse', 'Scraper']):
                        continue
                    valid_items.append(text)
            
            if valid_items:
                # 添加平台emoji
                platform_emojis = {
                    "Weibo": "📱", "微博": "📱",
                    "Douyin": "🎵", "抖音": "🎵", 
                    "Twitter": "🐦", "推特": "🐦",
                    "Baidu": "🔍", "百度": "🔍",
                    "Zhihu": "❓", "知乎": "❓",
                    "Bilibili": "📺", "B站": "📺",
                    "Xiaohongshu": "📕", "小红书": "📕",
                    "Kuaishou": "⚡", "快手": "⚡",
                    "Xigua": "🍉", "西瓜视频": "🍉",
                    "Xueqiu": "📈", "雪球": "📈",
                    "Reddit": "👽",
                    "YouTube": "🎬",
                    "StackOverflow": "💻"
                }
                
                emoji = platform_emojis.get(platform_name, "🔥")
                markdown_content += f"## {emoji} {platform_name}\n"
                
                # 显示有效条目
                for item in valid_items:
                    markdown_content += f"- {item}\n"
                
                # 如果实际条数少于显示条数，添加统计
                if len(valid_items) < len(items):
                    markdown_content += f"*（共 {len(valid_items)} 条有效数据）*\n"
                
                markdown_content += "\n"
        
        # 发送到WxPusher
        url = "https://wxpusher.zjiecode.com/api/send/message"
        data = {
            "appToken": WXPUSHER_APP_TOKEN,
            "content": markdown_content[:5000],  # WxPusher支持更长内容
            "summary": subject[:100],
            "contentType": 3,  # 3表示Markdown
            "topicIds": [],
            "uids": [WXPUSHER_USER_UID],
            "url": ""
        }
        
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        if result.get('code') == 1000:
            print("WxPusher send success")
            return True
        else:
            print(f"WxPusher failed: {result}")
            return False
            
    except Exception as e:
        print(f"WxPusher Error: {e}")
        return False

def send_wechat(subject, content):
    """
    Try sending with configured providers.
    Priority: WxPusher > WeChat Test Account > PushPlus > ServerChan
    """
    # First try WxPusher (支持长文本)
    if all([WXPUSHER_APP_TOKEN, WXPUSHER_USER_UID]):
        return send_wxpusher(subject, content)
    # Then try WeChat Test Account
    elif all([WECHAT_APPID, WECHAT_APPSECRET, WECHAT_TEMPLATE_ID, WECHAT_USER_OPENID]):
        return send_wechat_test(subject, content)
    # Then try PushPlus
    elif PUSHPLUS_TOKEN:
        return send_pushplus(subject, content)
    # Finally try ServerChan
    elif SERVERCHAN_KEY:
        return send_serverchan(subject, content)
    else:
        print("No Push notification service configured.")
        return False
