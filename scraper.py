import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import os
import webbrowser

def generate_aetheris_prime_v2():
    # الهوية الجديدة: Aetheris Prime - النسخة الاحترافية
    rss_url = "https://hbrarabic.com/feed/rss/"
    ad_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
    
    # رؤوس HTTP المخصصة التي زودتني بها
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,video/*;q=0.9,*/*;q=0.8',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'cross-site',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Ch-Ua': '"Google Chrome";v="124", "Not:A-Brand";v="8", "Chromium";v="124"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://www.google.com',
        'Range': 'bytes=0-'
    }

    try:
        print("⏳ جاري سحب المحتوى باستخدام البروتوكول المحدث...")
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:13]

        if not items:
            print("❌ لم يتم العثور على محتوى. تأكد من جودة اتصال الإنترنت.")
            return

        # استخراج بيانات المقال الرئيسي (Hero Section)
        hero = items[0]
        hero_title = hero.title.text
        hero_link = hero.link.text
        hero_desc = re.sub('<[^<]+?>', '', hero.description.text)[:220] + "..." if hero.description else ""
        
        # جلب صورة المقال الرئيسي
        hero_img = "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1600"
        enclosure = hero.find('enclosure')
        if enclosure: hero_img = enclosure.get('url')

        # بناء شبكة المقالات الثانوية
        articles_grid = ""
        for i, item in enumerate(items[1:]):
            title = item.title.text
            link = item.link.text
            img = ""
            enc = item.find('enclosure')
            if enc: img = enc.get('url')
            if not img: img = f"https://picsum.photos/seed/{i+99}/600/400"
            
            summary = re.sub('<[^<]+?>', '', item.description.text)[:100] + "..." if item.description else ""
            
            articles_grid += f'''
            <div class="glass-card">
                <div class="card-img" style="background-image: url('{img}')"></div>
                <div class="card-body">
                    <h3>{title}</h3>
                    <p>{summary}</p>
                    <div class="card-footer">
                        <a href="{link}" target="_blank" class="main-btn">إقرأ الآن</a>
                        <a href="{ad_link}" target="_blank" class="ad-btn">إعلان</a>
                    </div>
                </div>
            </div>'''

        # هيكل الـ HTML (تم الحفاظ على التصميم السينمائي)
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aetheris Prime | HBR Edition</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;500;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --prime: #00f2fe; --accent: #7117ea; --bg: #050505;
            --glass: rgba(255, 255, 255, 0.03); --border: rgba(255, 255, 255, 0.1);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: 'Tajawal', sans-serif; }}
        body {{ background: var(--bg); color: #fff; overflow-x: hidden; }}
        .hero {{
            height: 75vh; width: 100%;
            background: linear-gradient(to bottom, rgba(5,5,5,0.1), var(--bg)), url('{hero_img}');
            background-size: cover; background-position: center;
            display: flex; align-items: flex-end; padding: 0 8% 60px;
        }}
        .hero-content {{ max-width: 850px; animation: fadeInUp 0.8s ease-out; }}
        .hero-tag {{ background: var(--prime); color: #000; padding: 4px 12px; font-weight: 800; border-radius: 4px; font-size: 13px; text-transform: uppercase; }}
        .hero-title {{ font-size: clamp(22px, 5vw, 44px); margin: 15px 0; line-height: 1.3; font-weight: 800; }}
        .hero-desc {{ color: #bbb; font-size: 17px; margin-bottom: 25px; line-height: 1.6; }}
        .container {{ max-width: 1400px; margin: -40px auto 80px; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .glass-card {{
            background: var(--glass); backdrop-filter: blur(12px);
            border: 1px solid var(--border); border-radius: 15px; overflow: hidden;
            transition: 0.3s ease;
        }}
        .glass-card:hover {{ transform: translateY(-8px); border-color: var(--prime); }}
        .card-img {{ height: 190px; background-size: cover; background-position: center; }}
        .card-body {{ padding: 20px; }}
        .card-body h3 {{ font-size: 17px; margin-bottom: 12px; min-height: 48px; line-height: 1.4; }}
        .card-body p {{ font-size: 13px; color: #999; margin-bottom: 20px; height: 55px; overflow: hidden; }}
        .card-footer {{ display: flex; gap: 8px; }}
        .main-btn {{
            flex: 2; padding: 10px; text-align: center; text-decoration: none;
            background: linear-gradient(45deg, var(--prime), var(--accent));
            color: #fff; border-radius: 8px; font-weight: bold; font-size: 14px;
        }}
        .ad-btn {{
            flex: 1; padding: 10px; text-align: center; text-decoration: none;
            border: 1px solid var(--border); color: #fff; border-radius: 8px; font-size: 11px; transition: 0.3s;
        }}
        .ad-btn:hover {{ background: #fff; color: #000; }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        footer {{ text-align: center; padding: 40px; border-top: 1px solid var(--border); color: #444; font-size: 13px; }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <span class="hero-tag">أحدث مقال إداري</span>
            <h1 class="hero-title">{hero_title}</h1>
            <p class="hero-desc">{hero_desc}</p>
            <a href="{hero_link}" target="_blank" class="main-btn" style="padding: 14px 45px; border-radius: 25px; display: inline-block;">قراءة المقال بالكامل</a>
        </div>
    </section>

    <div class="container">
        <div class="grid">{articles_grid}</div>
    </div>

    <footer>
        <p>Aetheris Prime - High Performance Version</p>
        <p style="margin-top:5px;">Source: HBR Arabic | Ad-Placement Active</p>
    </footer>
</body>
</html>'''

        # حفظ الملف
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        path = os.path.join(desktop, "Aetheris_Prime_V2.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_html)

        print(f"✅ تم بنجاح! الرؤوس الجديدة مفعلة الآن.")
        print(f"📄 المسار الجديد: {path}")
        webbrowser.open(f"file://{path}")

    except Exception as e:
        print(f"❌ حدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    generate_aetheris_prime_v2()
