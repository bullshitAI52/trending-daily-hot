#!/usr/bin/env python3
"""
测试WxPusher推送
"""
import requests
import json
import time

# 配置信息
APP_TOKEN = "AT_VlNRYsrz9NgWCwuKtEIcQCIyhaOJH7pI"
USER_UID = "UID_sPgen3dJSu6TjZ9KVTFKa8aox01o"

def test_wxpusher():
    """发送测试消息"""
    print("发送测试消息到WxPusher...")
    
    # 测试消息内容
    test_content = f"""# 🧪 测试消息

**时间**: {time.strftime('%Y-%m-%d %H:%M:%S')}

## 📋 测试项目
1. 热点聚合推送系统测试
2. WxPusher连接测试
3. Markdown格式测试

## ✅ 测试要点
- 消息是否能正常接收
- Markdown格式是否正常显示
- 推送延迟情况

## 🔍 后续步骤
如果收到此消息，请回复"收到测试"
"""
    
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": APP_TOKEN,
        "content": test_content,
        "summary": "测试消息 | 热点推送系统",
        "contentType": 3,  # Markdown格式
        "topicIds": [],
        "uids": [USER_UID],
        "url": ""
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        result = response.json()
        
        print(f"响应状态: {response.status_code}")
        print(f"响应内容: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get('code') == 1000:
            print("✅ 测试消息发送成功！")
            print(f"📨 消息ID: {result.get('data', {}).get('messageId')}")
            print("📱 请检查微信'WxPusher'公众号消息")
        else:
            print(f"❌ 发送失败: {result.get('msg')}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    test_wxpusher()