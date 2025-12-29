# main.py
import datetime
from scraper import fetch_weibo_hot, fetch_douyin_hot, fetch_xhs_hot, fetch_twitter_hot
from notifier import send_wechat
from config import ENABLE_WEIBO, ENABLE_DOUYIN, ENABLE_XHS, ENABLE_TWITTER

def generate_html(data_dict):
    """
    Generates a simple HTML report
    """
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    html = f"<h3>📅 Hot Trends Report - {today}</h3>"
    
    for platform, items in data_dict.items():
        html += f"<h4>🔥 {platform}</h4><ul>"
        if not items:
            html += "<li>No data available</li>"
        else:
            for i, item in enumerate(items):
                title = item.get('title', 'N/A')
                url = item.get('url', '#')
                hot = item.get('hot', '')
                hot_str = f" ({hot})" if hot else ""
                html += f"<li>{i+1}. <a href='{url}'>{title}</a>{hot_str}</li>"
        html += "</ul>"
        
    return html

def main():
    print("Fetching hot trends...")
    data = {}
    
    if ENABLE_WEIBO:
        print("Scraping Weibo...")
        data["Weibo"] = fetch_weibo_hot()
        
    if ENABLE_DOUYIN:
        print("Scraping Douyin...")
        data["Douyin"] = fetch_douyin_hot()
        
    if ENABLE_XHS:
        print("Scraping Xiaohongshu...")
        # XHS is limited, currently returns a placeholder or empty
        data["Xiaohongshu"] = fetch_xhs_hot()
        
    if ENABLE_TWITTER:
        print("Scraping Twitter...")
        data["Twitter"] = fetch_twitter_hot()
        
    # Generate Report
    print("Generating report...")
    html_content = generate_html(data)
    
    # Send
    print("Sending notification...")
    subject = f"Trending Report {datetime.datetime.now().strftime('%m-%d')}"
    succeeded = send_wechat(subject, html_content)
    
    if not succeeded:
        print("\n=== DEBUG: Output Content (since send failed) ===")
        # Print a snippet if send failed, so user can see it works locally
        print(html_content[:500] + "...")

if __name__ == "__main__":
    main()
