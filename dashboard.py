from flask import Flask, render_template_string
from scanner import run_scan
from report import generate_report

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="fa">
<head>
  <meta charset="UTF-8">
  <title>📊 داشبورد امنیتی بات</title>
  <style>
    body { font-family: 'Vazir', sans-serif; background-color: #111; color: #eee; padding: 2em; }
    .status { font-size: 1.2em; margin: 0.5em 0; }
    .✅ { color: #4caf50; }
    .❌ { color: #f44336; }
    .⚠️ { color: #ff9800; }
    h2 { color: #00e6e6; }
    .section { border-left: 4px solid #00e6e6; padding-left: 1em; margin-top: 2em; }
  </style>
</head>
<body>
  <h2>📡 نتایج اسکن برای @{{ target }}</h2>
  <div class="section">
    {% for cat, tests in categorized.items() %}
      <h3>{{ cat }}</h3>
      {% for test in tests %}
        <div class="status {{ test.status }}">● {{ test.test }} — {{ test.status }} <br><small>{{ test.details }}</small></div>
      {% endfor %}
    {% endfor %}
  </div>
</body>
</html>
"""

@app.route("/scan/<target>")
def show_dashboard(target):
    results = run_scan(target, "توکن-بات-رو-اینجا-بذار")
    parsed = generate_report(results, output_type="json")
    parsed_obj = eval(parsed)  # برای ساده‌سازی نمایش، JSON رو تبدیل کردیم به dict

    return render_template_string(TEMPLATE,
        target=target,
        categorized=parsed_obj["details"]
    )

if __name__ == "__main__":
    app.run(port=8585, debug=True)