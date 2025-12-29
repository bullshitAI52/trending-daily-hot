# config.py
import os

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
ENABLE_TWITTER = True
ENABLE_BAIDU = True
ENABLE_ZHIHU = True
ENABLE_BILIBILI = True
ENABLE_KUAISHOU = True
ENABLE_XIGUA = True
ENABLE_LINUXDO = True
ENABLE_52POJIE = False
ENABLE_YOUTUBE = True
ENABLE_XUEQIU = True
ENABLE_REDDIT = True
ENABLE_STACKOVERFLOW = True

# Cookies & Tokens (Required for strict platforms)
# Login to web version -> F12 -> Network -> Copy 'Cookie' string
XHS_COOKIE = os.getenv("XHS_COOKIE", "") 
ZHIHU_COOKIE = os.getenv("ZHIHU_COOKIE", "")
KUAISHOU_COOKIE = os.getenv("KUAISHOU_COOKIE", "")
TWITTER_COOKIE = os.getenv("TWITTER_COOKIE", "") # Not used yet, complex

# Scheduling Configuration (for daily morning/evening reports)
# Use cron to schedule automatic runs:
# 1. Morning report at 8:30 AM: 30 8 * * * cd /path/to/cadname && python3 main.py
# 2. Evening report at 8:30 PM: 30 20 * * * cd /path/to/cadname && python3 main.py
# 
# Enable/disable platforms by setting ENABLE_* variables above to True/False
# Configure push services by setting PUSHPLUS_TOKEN or SERVERCHAN_KEY
# Set cookies for platforms that require login (Xiaohongshu, Zhihu, etc.)

