# main.py
import datetime
from scraper import fetch_weibo_hot, fetch_douyin_hot, fetch_xhs_hot, fetch_twitter_hot, fetch_baidu_hot, fetch_zhihu_hot, fetch_bilibili_hot, fetch_kuaishou_hot, fetch_xigua_hot, fetch_linuxdo_hot, fetch_52pojie_hot, fetch_youtube_hot, fetch_xueqiu_hot, fetch_reddit_hot, fetch_stackoverflow_hot
from notifier import send_wechat
from config import ENABLE_WEIBO, ENABLE_DOUYIN, ENABLE_XHS, ENABLE_TWITTER, ENABLE_BAIDU, ENABLE_ZHIHU, ENABLE_BILIBILI, ENABLE_KUAISHOU, ENABLE_XIGUA, ENABLE_LINUXDO, ENABLE_52POJIE, ENABLE_YOUTUBE, ENABLE_XUEQIU, ENABLE_REDDIT, ENABLE_STACKOVERFLOW

def generate_html(data_dict, time_period="morning"):
    """
    Generates HTML report optimized for WeChat Official Account.
    Each platform shows top 15 items only.
    """
    # Determine time period text
    period_text = "早安·热点速递 🌅" if time_period == "morning" else "晚安·热点盘点 🌙"
    time_str = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M")
    
    # WeChat-friendly HTML with inline styles
    html = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif; line-height: 1.6; color: #333; max-width: 680px; margin: 0 auto;">
    <div style="text-align: center; padding: 20px 0; border-bottom: 2px solid #e6e6e6;">
        <h1 style="margin: 0; font-size: 24px; color: #2c3e50;">{period_text}</h1>
        <p style="margin: 5px 0 0; font-size: 14px; color: #7f8c8d;">{time_str}</p>
    </div>
"""
    
    platform_emojis = {
        "Weibo": "📱",
        "Douyin": "🎵", 
        "Xiaohongshu": "📕",
        "Twitter": "🐦",
        "Baidu": "🔍",
        "Zhihu": "❓",
        "Bilibili": "📺",
        "Kuaishou": "⚡",
        "Xigua": "🍉",
        "Linux.do": "🐧",
        "52pojie": "🔓",
        "YouTube": "🎬",
        "Xueqiu": "📈",
        "Reddit": "👽",
        "StackOverflow": "💻"
    }
    
    for platform, items in data_dict.items():
        emoji = platform_emojis.get(platform, "🔥")
        
        html += f"""
    <div style="margin: 25px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #3498db;">
        <h2 style="margin: 0 0 12px 0; font-size: 18px; color: #2c3e50;">
            {emoji} {platform}
        </h2>
"""
        
        if not items:
            html += """
        <p style="margin: 0; color: #95a5a6; font-size: 14px;">暂无数据</p>
"""
        else:
            # Show only top 15 items
            top_items = items[:15]
            html += """
        <ul style="margin: 0; padding: 0; list-style: none;">
"""
            for i, item in enumerate(top_items):
                title = item.get('title', 'N/A').strip()
                url = item.get('url', '#')
                hot = item.get('hot', '').strip()
                
                # Truncate long titles for WeChat
                if len(title) > 30:
                    title = title[:27] + "..."
                
                # Rank styling
                rank_color = "#e74c3c" if i < 3 else "#3498db" if i < 6 else "#7f8c8d"
                
                # Hot value styling
                hot_html = ""
                if hot:
                    hot_html = f'<span style="font-size: 12px; color: #e74c3c; margin-left: 8px;">{hot}</span>'
                
                html += f"""
            <li style="margin: 8px 0; padding: 0;">
                <span style="display: inline-block; width: 20px; height: 20px; line-height: 20px; text-align: center; background: {rank_color}; color: white; border-radius: 3px; font-size: 12px; margin-right: 8px;">{i+1}</span>
                <a href="{url}" style="color: #2c3e50; text-decoration: none; font-size: 15px;">{title}</a>
                {hot_html}
            </li>
"""
            html += """
        </ul>
"""
        
        html += """
    </div>
"""
    
    html += """
    <div style="text-align: center; padding: 20px 0; margin-top: 20px; border-top: 1px solid #e6e6e6; color: #95a5a6; font-size: 12px;">
        <p style="margin: 0;">每日早晚推送 • 热点信息仅供参考</p>
        <p style="margin: 5px 0 0;">数据来源：各平台公开榜单</p>
    </div>
</div>
"""
    
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
        
    if ENABLE_BAIDU:
        print("Scraping Baidu...")
        data["Baidu"] = fetch_baidu_hot()
        
    if ENABLE_ZHIHU:
        print("Scraping Zhihu...")
        data["Zhihu"] = fetch_zhihu_hot()
        
    if ENABLE_BILIBILI:
        print("Scraping Bilibili...")
        data["Bilibili"] = fetch_bilibili_hot()
        
    if ENABLE_KUAISHOU:
        print("Scraping Kuaishou...")
        data["Kuaishou"] = fetch_kuaishou_hot()
        
    if ENABLE_XIGUA:
        print("Scraping Xigua...")
        data["Xigua"] = fetch_xigua_hot()
        
    if ENABLE_LINUXDO:
        print("Scraping Linux.do...")
        data["Linux.do"] = fetch_linuxdo_hot()
        
    if ENABLE_52POJIE:
        print("Scraping 52pojie...")
        data["52pojie"] = fetch_52pojie_hot()
        
    if ENABLE_YOUTUBE:
        print("Scraping YouTube...")
        data["YouTube"] = fetch_youtube_hot()
        
    if ENABLE_XUEQIU:
        print("Scraping Xueqiu...")
        data["Xueqiu"] = fetch_xueqiu_hot()
        
    if ENABLE_REDDIT:
        print("Scraping Reddit...")
        data["Reddit"] = fetch_reddit_hot()
        
    if ENABLE_STACKOVERFLOW:
        print("Scraping StackOverflow...")
        data["StackOverflow"] = fetch_stackoverflow_hot()
        
    # Determine time period
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour < 12:
        time_period = "morning"
        period_cn = "早安·热点速递"
    else:
        time_period = "evening"
        period_cn = "晚安·热点盘点"
    
    # Generate Report
    print(f"Generating {time_period} report...")
    html_content = generate_html(data, time_period)
    
    # Send
    print("Sending notification...")
    date_str = datetime.datetime.now().strftime("%m月%d日")
    subject = f"{period_cn} | {date_str}"
    succeeded = send_wechat(subject, html_content)
    
    if not succeeded:
        print("\n=== DEBUG: Output Content (since send failed) ===")
        # Print a snippet if send failed, so user can see it works locally
        print(html_content[:500] + "...")

if __name__ == "__main__":
    main()
