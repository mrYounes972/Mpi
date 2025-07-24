import smtplib
from email.mime.text import MIMEText

def send_alert(scan_results, admin_email):
    danger_keywords = ["SQLi", "XSS", "Inline Injection", "Token Fingerprint"]
    alerts = [r for r in scan_results if r["status"] == "❌" or any(k in r["test"] for k in danger_keywords)]

    if not alerts:
        return "🚩 مشکلی جدی شناسایی نشد."

    body = "\n".join([f"{r['test']} ➤ {r['status']}: {r['details']}" for r in alerts])
    msg = MIMEText(body)
    msg["Subject"] = "🚨 Bot Scan Alert"
    msg["From"] = "scanner@yourdomain.com"
    msg["To"] = admin_email

    try:
        server = smtplib.SMTP("smtp.yourdomain.com", 587)
        server.starttls()
        server.login("scanner@yourdomain.com", "رمز-عبور")
        server.sendmail(msg["From"], [msg["To"]], msg.as_string())
        server.quit()
        return f"✅ هشدار به {admin_email} ارسال شد."
    except Exception as e:
        return f"❌ خطا در ارسال هشدار: {e}"