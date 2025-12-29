# notifier.py
import requests
import json
from config import PUSHPLUS_TOKEN, SERVERCHAN_KEY

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

def send_wechat(subject, content):
    """
    Try sending with configured providers.
    """
    # Prefer PushPlus as it supports better HTML
    if PUSHPLUS_TOKEN:
        return send_pushplus(subject, content)
    elif SERVERCHAN_KEY:
        return send_serverchan(subject, content)
    else:
        print("No Push notification service configured.")
        return False
