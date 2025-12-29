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

# Cookies & Tokens (Required for strict platforms)
# Login to web version -> F12 -> Network -> Copy 'Cookie' string
XHS_COOKIE = os.getenv("XHS_COOKIE", "") 
TWITTER_COOKIE = os.getenv("TWITTER_COOKIE", "") # Not used yet, complex

