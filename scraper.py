import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random
import time

def generate_nexusvision_site():
    rss_url = "https://akhbaralaan.net/feed/rss/"

    # رؤوس HTTP محسنة لأحدث إصدار 2026
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
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
        'View-Transition': 'same-origin'
    }

    try:
        # إضافة تأخير عشوائي لمحاكاة سلوك بشري
        time.sleep(random.uniform(0.5, 2.0))

        # جلب المحتوى من RSS
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:24]  # زيادة عدد الأخبار إلى 24

        # إنشاء شريط الأخبار المتحرك
        ticker_items = " • ".join([item.title.text for item in items[:12]])

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

            # تنظيف الوصف وإزالة الوسوم
            clean_desc = re.sub('<[^<]+?>', '', description)[:180] + "..."

            # تحديد فئة الخبر
            category = ["حصري", "عاجل", "مهم", "رياضة", "سياسة", "اقتصاد"][i % 6]

            news_html += f'''
            <article class="nexus-card">
                <div class="category-badge {category.lower()}">{category}</div>
                <div class="card-image">
                    <img src="{img_url}" loading="lazy" alt="{title}" onerror="this.src='https://via.placeholder.com/800x500/1a1a1a/ffffff?text=NexusVision'">
                </div>
                <div class="card-content">
                    <h2 class="card-title">{title}</h2>
                    <p class="card-snippet">{clean_desc}</p>
                    <div class="meta-data">
                        <span class="date">🕒 {datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %z").strftime("%Y-%m-%d %H:%M")}</span>
                        <span class="views">👁 {random.randint(100, 5000)}</span>
                    </div>
                    <div class="action-area">
                        <a href="{link}" target="_blank" class="btn-nexus">قراءة المزيد</a>
                        <button class="btn-share" onclick="shareNews('{title}', '{link}')">مشاركة</button>
                    </div>
                </div>
            </article>'''

        # إنشاء الصفحة الكاملة مع اسم NexusVision
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="NexusVision - منصة أخبار moderne مع تصميم Glassmorphism">
    <meta name="keywords" content="أخبار, Glassmorphism, تصميم moderne, NexusVision">
    <title>NexusVision | منصة الأخبار الحديثة</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.06);
            --glass-border: rgba(255, 255, 255, 0.15);
            --primary: #00f2fe;
            --secondary: #ff0844;
            --accent: #a29bfe;
            --text-main: #ffffff;
            --text-secondary: rgba(255, 255, 255, 0.7);
        }}
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            background: linear-gradient(135deg, #0a0e2a, #1a1f3a, #2d3748);
            background-attachment: fixed;
            font-family: 'Cairo', sans-serif;
            color: var(--text-main);
            padding-top: 130px;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        header {{
            background: rgba(10, 14, 42, 0.7);
            backdrop-filter: blur(25px);
            padding: 15px 5%;
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 1000;
            border-bottom: 1px solid var(--glass-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-family: 'Poppins', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: #fff;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .logo-icon {{
            color: var(--primary);
            font-size: 28px;
        }}
        .logo-text {{
            background: linear-gradient(90deg, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
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
            color: white;
        }}
        .ticker-scroll {{
            white-space: nowrap;
            animation: scroll 90s linear infinite;
            padding: 0 20px;
            font-size: 14px;
        }}
        @keyframes scroll {{
            0% {{ transform: translateX(100%); }}
            100% {{ transform: translateX(-250%); }}
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto 50px;
            padding: 0 20px;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
        }}
        .nexus-card {{
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            position: relative;
        }}
        .nexus-card:hover {{
            transform: translateY(-12px);
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
        }}
        .category-badge {{
            position: absolute;
            top: 15px;
            right: 15px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 20px;
            z-index: 5;
            color: white;
        }}
        .category-badge.حصري {{ background: linear-gradient(90deg, #ff0844, #ff4d7e); }}
        .category-badge.عاجل {{ background: linear-gradient(90deg, #ff6b35, #f7931e); }}
        .category-badge.مهم {{ background: linear-gradient(90deg, #a29bfe, #d4c5fd); }}
        .category-badge.رياضة {{ background: linear-gradient(90deg, #00f2fe, #4facfe); }}
        .category-badge.سياسة {{ background: linear-gradient(90deg, #43e97b, #38f9d7); }}
        .category-badge.اقتصاد {{ background: linear-gradient(90deg, #ffd86f, #fc6262); }}
        .card-image {{
            height: 200px;
            overflow: hidden;
        }}
        .card-image img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
        }}
        .nexus-card:hover .card-image img {{
            transform: scale(1.07);
        }}
        .card-content {{
            padding: 20px;
        }}
        .card-title {{
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 12px;
            line-height: 1.4;
            color: var(--text-main);
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
            gap: 10px;
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
            border: none;
            cursor: pointer;
        }}
        .btn-nexus:hover {{
            transform: scale(1.03);
            box-shadow: 0 5px 15px rgba(0, 242, 254, 0.3);
        }}
        .btn-share {{
            background: rgba(255, 255, 255, 0.1);
            color: var(--text-main);
            border: 1px solid var(--glass-border);
            padding: 10px 15px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .btn-share:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: var(--primary);
            color: var(--primary);
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
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 15px;
        }}
        .social-links a {{
            color: var(--text-secondary);
            font-size: 20px;
            transition: all 0.3s;
        }}
        .social-links a:hover {{
            color: var(--primary);
            transform: translateY(-3px);
        }}
        @media (max-width: 768px) {{
            .container {{
                grid-template-columns: 1fr;
            }}
            body {{
                padding-top: 160px;
            }}
            .ticker-wrap {{
                top: 90px;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">
            <i class="fas fa-network-wired logo-icon"></i>
            <span class="logo-text">NexusVision</span>
        </a>
        <div class="search-icon">
            <i class="fas fa-search"></i>
        </div>
    </header>
    <div class="ticker-wrap">
        <div class="ticker-title"><i class="fas fa-bolt"></i> آخر الأخبار</div>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>
    <main class="container">
        {news_html}
    </main>
    <footer>
        <p>&copy; {datetime.now().year} NexusVision | منصة الأخبار الحديثة</p>
        <div class="social-links">
            <a href="#"><i class="fab fa-facebook-f"></i></a>
            <a href="#"><i class="fab fa-twitter"></i></a>
            <a href="#"><i class="fab fa-instagram"></i></a>
            <a href="#"><i class="fab fa-youtube"></i></a>
        </div>
    </footer>
    <script>
        function shareNews(title, url) {{
            if (navigator.share) {{
                navigator.share({{
                    title: title,
                    url: url
                }}).catch(err => {{
                    console.log("Error sharing:", err);
                }});
            }} else {{
                alert("ميزة المشاركة غير مدعومة في متصفحك الحالي");
            }}
        }}

        // إضافة تأثيرات إضافية
        document.addEventListener('DOMContentLoaded', function() {{
            const cards = document.querySelectorAll('.nexus-card');
            cards.forEach(card => {{
                card.addEventListener('mousemove', (e) => {{
                    const rect = card.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;

                    card.style.setProperty('--mouse-x', `${{x}}px`);
                    card.style.setProperty('--mouse-y', `${{y}}px`);
                }});
            }});
        }});
    </script>
</body>
</html>'''
        with open("nexusvision.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("✅ تم إنشاء موقع NexusVision بنجاح! افتح ملف nexusvision.html")

    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    generate_nexusvision_site()
