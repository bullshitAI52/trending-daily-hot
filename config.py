# No change
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# Push Service Configuration
# Get your token from http://www.pushplus.plus/
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN", "") 
# Get your key from https://sct.ftqq.com/
SERVERCHAN_KEY = os.getenv("SERVERCHAN_KEY", "")

# Scraper Configuration
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Platform Switches
ENABLE_WEIBO = True
ENABLE_DOUYIN = True
ENABLE_XHS = True
ENABLE_TWITTER = False  # 暂时隐藏，以后完善
ENABLE_BAIDU = True
ENABLE_ZHIHU = True
ENABLE_BILIBILI = True
ENABLE_KUAISHOU = True
ENABLE_XIGUA = True
ENABLE_LINUXDO = False  # 暂时隐藏，以后完善
ENABLE_52POJIE = False
ENABLE_YOUTUBE = False
ENABLE_FINANCE = True
ENABLE_REDDIT = False
ENABLE_STACKOVERFLOW = False
ENABLE_XIANYU = True
ENABLE_XMFISH = True
ENABLE_NETEASE = True

# Cookies & Tokens (Required for strict platforms)
# Login to web version -> F12 -> Network -> Copy 'Cookie' string
XHS_COOKIE = os.getenv("XHS_COOKIE", "") 
ZHIHU_COOKIE = os.getenv("ZHIHU_COOKIE", "")
KUAISHOU_COOKIE = os.getenv("KUAISHOU_COOKIE", "")
TWITTER_COOKIE = os.getenv("TWITTER_COOKIE", "") # Not used yet, complex

# WeChat Test Account Configuration
# Get from https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login
WECHAT_APPID = os.getenv("WECHAT_APPID", "")
WECHAT_APPSECRET = os.getenv("WECHAT_APPSECRET", "")
WECHAT_TEMPLATE_ID = os.getenv("WECHAT_TEMPLATE_ID", "")
WECHAT_USER_OPENID = os.getenv("WECHAT_USER_OPENID", "")

# WxPusher Configuration (推荐，支持长文本)
# Get from https://wxpusher.zjiecode.com/
WXPUSHER_APP_TOKEN = os.getenv("WXPUSHER_APP_TOKEN", "")
WXPUSHER_USER_UID = os.getenv("WXPUSHER_USER_UID", "")

# Scheduling Configuration (for daily morning/evening reports)
# Use cron to schedule automatic runs:
# 1. Morning report at 8:30 AM: 30 8 * * * cd /path/to/cadname && python3 main.py
# 2. Evening report at 8:30 PM: 30 20 * * * cd /path/to/cadname && python3 main.py
# 
# Enable/disable platforms by setting ENABLE_* variables above to True/False
# Configure push services by setting PUSHPLUS_TOKEN or SERVERCHAN_KEY
# Set cookies for platforms that require login (Xiaohongshu, Zhihu, etc.)

