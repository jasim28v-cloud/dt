import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import random
import time

def generate_nexusvision_site():
    rss_url = "https://akhbaralaan.net/feed/rss/"

    # رؤوس HTTP كاملة ومحدثة لأحدث معايير 2026
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'application/xml, text/xml, */*; q=0.01',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Ch-Ua': '"Microsoft Edge";v="126", "Not(A:Brand";v="8", "Chromium";v="126"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
        'Priority': 'u=1, i',
        'View-Transition': 'same-origin',
        'TE': 'trailers'
    }

    try:
        # إضافة تأخير عشوائي لمحاكاة سلوك بشري
        time.sleep(random.uniform(0.5, 1.5))

        # جلب المحتوى من RSS
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:12]  # أخذ أول 12 خبر

        # إنشاء شريط الأخبار المتحرك
        ticker_items = " • ".join([item.title.text for item in items[:8]])

        # بناء محتوى الأخبار
        news_html = ""
        for i, item in enumerate(items):
            title = item.title.text
            link = item.link.text
            pub_date = item.pubdate.text if item.pubdate else datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")

            # استخراج الصورة إذا كانت موجودة
            description = item.description.text if item.description else ""
            img_match = re.search(r'<img[^>]+src="([^">]+)"', description)
            img_url = img_match.group(1) if img_match else f"https://picsum.photos/800/500?random={i}"

            # تنظيف الوصف
            clean_desc = re.sub('<[^<]+?>', '', description)[:150] + "..."

            # تحديد فئة الخبر
            category = ["حصري", "عاجل", "مهم", "رياضة", "سياسة", "اقتصاد"][i % 6]

            news_html += f'''
            <article class="nexus-card">
                <div class="category-badge {category.lower()}">{category}</div>
                <div class="card-image">
                    <img src="{img_url}" loading="lazy" alt="{title}" onerror="this.src=\'https://via.placeholder.com/800x500/1a1a1a/ffffff?text=NexusVision\'">
                </div>
                <div class="card-content">
                    <h2 class="card-title">{title}</h2>
                    <p class="card-snippet">{clean_desc}</p>
                    <div class="meta-data">
                        <span>🕒 {datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M")}</span>
                        <span>👁 {random.randint(100, 5000)}</span>
                    </div>
                    <div class="action-area">
                        <a href="{link}" target="_blank" class="btn-nexus">قراءة المزيد</a>
                    </div>
                </div>
            </article>'''

        # إنشاء الصفحة الكاملة مع جميع العناصر الضرورية
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="NexusVision - منصة أخبار moderne مع تصميم Glassmorphism">
    <title>NexusVision | منصة الأخبار الحديثة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.08);
            --glass-border: rgba(255, 255, 255, 0.15);
            --primary: #00f2fe;
            --secondary: #ff0844;
            --text-main: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: linear-gradient(135deg, #0a0e2a, #1a1f3a);
            font-family: 'Cairo', sans-serif;
            color: var(--text-main);
            padding-top: 120px;
            min-height: 100vh;
        }}
        header {{
            background: rgba(10, 14, 42, 0.7);
            backdrop-filter: blur(20px);
            padding: 15px 5%;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            border-bottom: 1px solid var(--glass-border);
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .logo {{
            font-size: 24px;
            font-weight: 700;
            color: #fff;
            text-shadow: 0 0 10px var(--primary);
        }}
        .ticker-wrap {{
            position: fixed;
            top: 60px;
            width: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(15px);
            color: #fff;
            overflow: hidden;
            height: 45px;
            display: flex;
            align-items: center;
            z-index: 999;
        }}
        .ticker-title {{
            background: var(--secondary);
            padding: 0 20px;
            font-weight: 700;
            height: 100%;
            display: flex;
            align-items: center;
            font-size: 14px;
        }}
        .ticker-scroll {{
            white-space: nowrap;
            animation: scroll 90s linear infinite;
            padding: 0 20px;
            font-size: 14px;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-200%); }}
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto 50px;
            padding: 0 20px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 25px;
        }}
        .nexus-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(15px);
            border-radius: 15px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease;
        }}
        .nexus-card:hover {{
            transform: translateY(-10px);
        }}
        .category-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 5px 10px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 15px;
            color: white;
        }}
        .category-badge.حصري {{ background: var(--secondary); }}
        .category-badge.عاجل {{ background: #ff6b35; }}
        .category-badge.مهم {{ background: #a29bfe; }}
        .category-badge.رياضة {{ background: var(--primary); }}
        .category-badge.سياسة {{ background: #43e97b; }}
        .category-badge.اقتصاد {{ background: #ffd86f; }}
        .card-image {{
            height: 200px;
            overflow: hidden;
        }}
        .card-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s;
        }}
        .nexus-card:hover .card-image img {{
            transform: scale(1.05);
        }}
        .card-content {{
            padding: 15px;
        }}
        .card-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .card-snippet {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        .meta-data {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: var(--text-secondary);
            margin-bottom: 15px;
            padding-top: 10px;
            border-top: 1px solid var(--glass-border);
        }}
        .action-area {{
            display: flex;
        }}
        .btn-nexus {{
            flex: 1;
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            color: #fff;
            text-decoration: none;
            text-align: center;
            padding: 10px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        .btn-nexus:hover {{
            transform: scale(1.03);
        }}
        footer {{
            text-align: center;
            padding: 30px;
            color: var(--text-secondary);
            font-size: 13px;
            border-top: 1px solid var(--glass-border);
            background: rgba(10, 14, 42, 0.3);
            backdrop-filter: blur(10px);
        }}
        @media (max-width: 768px) {{
            .container {{ grid-template-columns: 1fr; }}
            body {{ padding-top: 150px; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="logo">NexusVision</div>
    </header>
    <div class="ticker-wrap">
        <div class="ticker-title">أهم الأخبار</div>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>
    <main class="container">
        {news_html}
    </main>
    <footer>
        <p>© {datetime.now().year} NexusVision | منصة الأخبار الحديثة</p>
    </footer>
</body>
</html>'''

        # حفظ الملف في مسار واضح على سطح المكتب
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        file_path = os.path.join(desktop_path, "nexusvision.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"✅ تم إنشاء موقع NexusVision بنجاح!")
        print(f"يمكنك العثور على الملف في: {file_path}")
        print(f"افتح الملف باستخدام متصفحك المفضل للبدء في التصفح.")

    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في جلب البيانات: {e}")
        print("قد يكون هناك حظر للطلب من قبل الموقع أو مشكلة في الاتصال بالإنترنت.")
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    generate_nexusvision_site()
