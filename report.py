import json, datetime

def generate_report(scan_results, output_type="text"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary = {"✅": 0, "❌": 0, "⚠️": 0}
    categorized = {}

    for result in scan_results:
        status = result["status"]
        test_name = result["test"]
        summary[status] = summary.get(status, 0) + 1
        cat = test_name.split()[0]
        if cat not in categorized:
            categorized[cat] = []
        categorized[cat].append(result)

    if output_type == "json":
        return json.dumps({"timestamp": ts, "summary": summary, "details": categorized}, indent=2)

    elif output_type == "html":
        html = f"<h2>📊 Bot Scanner Report — {ts}</h2><ul>"
        html += f"<li>✅ Passed: {summary['✅']}</li><li>❌ Failed: {summary['❌']}</li><li>⚠️ Risky: {summary['⚠️']}</li></ul><hr>"
        for cat, items in categorized.items():
            html += f"<h3>{cat}</h3><ul>"
            for item in items:
                html += f"<li><b>{item['test']}</b>: {item['status']}<br><i>{item['details']}</i></li>"
            html += "</ul><hr>"
        return html

    else:  # Plain Text
        report = [f"📄 Scan Report — {ts}", f"✅: {summary['✅']}, ❌: {summary['❌']}, ⚠️: {summary['⚠️']}"]
        for cat, items in categorized.items():
            report.append(f"\n— {cat} —")
            for item in items:
                line = f"{item['test']} [{item['status']}]"
                if item['details'] != "—":
                    line += f" ➤ {item['details']}"
                report.append(line)
        return "\n".join(report)