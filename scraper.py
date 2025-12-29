# scraper.py
import requests
import json
import re
from config import USER_AGENT, XHS_COOKIE
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()

def get_headers():
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

def fetch_weibo_hot():
    """
    Fetches Weibo Hot Search List.
    Uses s.weibo.com/top/summary which is often easier to scrape than the AJAX API without login.
    """
    url = "https://s.weibo.com/top/summary"
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        hot_list = []
        rows = soup.select('section.list tr')
        
        for row in rows:
            td_keyword = row.select_one('td.td-02')
            if not td_keyword:
                continue
                
            a_tag = td_keyword.find('a')
            if not a_tag:
                continue
                
            title = a_tag.get_text().strip()
            link = "https://s.weibo.com" + a_tag['href']
            
            # Hot value
            span = td_keyword.find('span')
            hot = span.get_text().strip() if span else "Top"
            
            # Skip the 'Top' pinned item if it has no hot value usually
            hot_list.append({
                "title": title,
                "url": link,
                "hot": hot
            })
            
        return hot_list[:20]
    except Exception as e:
        print(f"Error fetching Weibo hot: {e}")
        return []

def fetch_douyin_hot():
    """
    Fetches Douyin Hot List (Billboard).
    """
    # Using the DailyHotApi logic source which is often: https://www.douyin.com/aweme/v1/web/hot/search/list/
    # But this requires signatures often.
    # We will try a known public workaround or the same endpoint.
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/"
    headers = get_headers()
    headers['Referer'] = 'https://www.douyin.com/billboard/'
    # A dummy cookie sometimes helps pass basic checks
    headers['Cookie'] = 's_v_web_id=verify_leytkxgn_kvO5k9J5_3b9j_4b8f_8d5f_3b9j3b9j3b9j;' 
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        hot_list = []
        if 'data' in data and 'word_list' in data['data']:
            for item in data['data']['word_list']:
                title = item.get('word', '')
                link = f"https://www.douyin.com/search/{title}"
                hot_value = item.get('hot_value', 0)
                
                hot_list.append({
                    "title": title,
                    "url": link,
                    "hot": str(hot_value)
                })
        return hot_list[:20]
    except Exception as e:
        print(f"Error fetching Douyin hot: {e}")
        return []

def fetch_xhs_hot():
    """
    Fetches Xiaohongshu (RedNote) Hot List.
    Requires Cookie!
    """
    if not XHS_COOKIE:
        return [{"title": "XHS Config Required: Please fill XHS_COOKIE in config.py", "url": "", "hot": ""}]
        
    url = "https://www.xiaohongshu.com/explore"
    headers = get_headers()
    headers['Cookie'] = XHS_COOKIE
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # XHS often embeds initial state in specific script tags
        # But 'explore' page might just render tiles.
        # Hot content is hard to distinguish without API.
        # Let's try to find tiles with high likes (Mocking "Hot" behavior by fetching feed)
        
        hot_list = []
        sections = soup.select('.feed-container .note-item')
        if not sections:
             # Fallback: Try to parse window.__INITIAL_STATE__
             script = soup.find('script', string=re.compile('window.__INITIAL_STATE__'))
             if script:
                 json_str = script.string.replace('window.__INITIAL_STATE__=', '').strip().replace('undefined', 'null')
                 # This parsing is fragile.
                 # Simplified: Just tell user we need scraping API if visual parsing fails.
                 pass

        # Since XHS is tough, we simply return a message for now if visual parsing fails.
        if not hot_list:
             hot_list.append({"title": "XHS Scraper: Could not parse feed (Check Cookie)", "url": "", "hot": ""})
             
        return hot_list[:20]
    except Exception as e:
        print(f"Error fetching XHS hot: {e}")
        return [{"title": "XHS Error", "url": "", "hot": str(e)}]

def fetch_twitter_hot():
    """
    Fetches Twitter Trends.
    Uses 'nitter' instances if available or trends24 scraping.
    """
    # Using trends24.in which is HTML based.
    url = "https://trends24.in/china/" # You can change to 'worldwide' or other
    headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 404:
             # Try root
             url = "https://trends24.in/"
             response = requests.get(url, headers=headers, timeout=10)
             
        soup = BeautifulSoup(response.text, 'html.parser')
        
        hot_list = []
        # First list is usually 'now'
        trend_card = soup.select_one('.trend-card')
        if trend_card:
            items = trend_card.select('li a')
            for item in items:
                title = item.get_text().strip()
                link = item['href']
                hot_list.append({
                    "title": title,
                    "url": link,
                    "hot": "Trending"
                })
        
        if not hot_list:
             return [{"title": "Twitter Scraper: Could not find trends via trends24.in", "url": "", "hot": ""}]
             
        return hot_list[:20]
    except Exception as e:
        print(f"Error fetching Twitter hot: {e}")
        return [{"title": "Twitter Error", "url": "", "hot": str(e)}]

if __name__ == "__main__":
    print("Testing Scrapers...")
    # ... (Tested in separate runs)
