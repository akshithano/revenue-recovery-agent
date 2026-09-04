import csv
from datetime import datetime

with open("audit_trail.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

for r in rows:
    r["amount"] = float(r["amount"])
    r["amount_recovered"] = float(r["amount_recovered"])

total_at_risk = sum(r["amount"] for r in rows)
total_recovered = sum(r["amount_recovered"] for r in rows)
recovery_rate = (total_recovered / total_at_risk) * 100 if total_at_risk else 0
escalated_count = sum(1 for r in rows if r["action_taken"] == "escalate_human")
nudged_count = sum(1 for r in rows if r["action_taken"] == "nudge")
retried_count = sum(1 for r in rows if r["action_taken"] == "retry")
messaged_count = sum(1 for r in rows if r.get("ai_message"))

OUTCOME_COLOR = {
    "recovered": "#7FE0A8",
    "escalated": "#E0B36C",
    "still_failed": "#E08C7F",
    "no_response": "#E08C7F",
    "no_action": "#7A7D8A",
}

def row_html(i, r):
    color = OUTCOME_COLOR.get(r["outcome"], "#7A7D8A")
    zebra = "row-alt" if i % 2 else ""
    return f"""
    <tr class="{zebra}">
      <td class="mono dim">{r['txn_id']}</td>
      <td>{r['customer']}</td>
      <td class="mono num">{r['amount']:,.2f}</td>
      <td class="dim">{r['failure_type'].replace('_',' ')}</td>
      <td class="dim">{r['action_taken'].replace('_',' ')}</td>
      <td class="mono" style="color:{color};">{r['outcome'].replace('_',' ')}</td>
      <td class="mono num" style="color:{color if r['amount_recovered'] else '#7A7D8A'};">{r['amount_recovered']:,.2f}</td>
    </tr>"""

rows_html = "\n".join(row_html(i, r) for i, r in enumerate(rows))
run_time = datetime.now().strftime("%d %b %Y, %H:%M")

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Revenue Recovery — Batch Story</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    font-family: 'Fraunces', Georgia, serif;
    background: #12141A;
    color: #EDEBE4;
    margin: 0;
  }}
  .mono {{ font-family: 'IBM Plex Mono', monospace; }}
  .dim {{ color: #9A9CA8; }}

  .glow {{
    position: fixed;
    top: 50%;
    left: 50%;
    width: 900px;
    height: 900px;
    transform: translate(-50%, -50%);
    background: radial-gradient(circle, rgba(108,123,240,0.10) 0%, rgba(108,123,240,0) 65%);
    pointer-events: none;
    z-index: 0;
  }}

  .beat {{
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px;
    position: relative;
    z-index: 1;
  }}
  .beat .inner {{
    max-width: 720px;
    opacity: 0;
    transform: translateY(24px);
    transition: opacity 0.9s ease, transform 0.9s ease;
  }}
  .beat .inner.shown {{
    opacity: 1;
    transform: translateY(0);
  }}

  .eyebrow {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #6C7BF0;
    letter-spacing: 0.08em;
    margin-bottom: 22px;
  }}
  .beat h1 {{
    font-size: 44px;
    font-weight: 600;
    line-height: 1.25;
    margin: 0;
    letter-spacing: -0.01em;
  }}
  .beat h1 .num {{
    font-family: 'IBM Plex Mono', monospace;
    color: #EDEBE4;
  }}
  .beat h1 .accent {{
    color: #6C7BF0;
  }}
  .beat p.sub {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 13px;
    color: #9A9CA8;
    margin-top: 22px;
    line-height: 1.7;
  }}

  .stat-trio {{
    display: flex;
    gap: 50px;
    justify-content: center;
    margin-top: 6px;
  }}
  .stat-trio div {{
    text-align: center;
  }}
  .stat-trio .n {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 30px;
    color: #EDEBE4;
  }}
  .stat-trio .l {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #6C7078;
    margin-top: 8px;
    letter-spacing: 0.06em;
  }}

  .ledger-section {{
    position: relative;
    z-index: 1;
    max-width: 920px;
    margin: 0 auto;
    padding: 60px 40px 100px 40px;
  }}
  .ledger-section h2 {{
    font-family: 'IBM Plex Mono', monospace;
    font-size: 12px;
    color: #6C7078;
    letter-spacing: 0.08em;
    margin-bottom: 20px;
    text-align: center;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
  }}
  thead th {{
    text-align: left;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #6C7078;
    font-weight: 500;
    padding: 0 14px 10px 0;
    border-bottom: 1px solid #2A2D38;
  }}
  td {{
    padding: 9px 14px 9px 0;
    font-size: 13px;
    border-bottom: 1px solid #1D202A;
  }}
  .num {{ text-align: right; }}
  th.num {{ text-align: right; }}
  .row-alt {{ background: #171921; }}

  .scroll-hint {{
    position: absolute;
    bottom: 36px;
    left: 50%;
    transform: translateX(-50%);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #6C7078;
    letter-spacing: 0.1em;
    animation: bob 2s ease-in-out infinite;
  }}
  @keyframes bob {{
    0%, 100% {{ transform: translate(-50%, 0); }}
    50% {{ transform: translate(-50%, 6px); }}
  }}
</style>
</head>
<body>

<div class="glow"></div>

<div class="beat">
  <div class="inner shown">
    <div class="eyebrow">REVENUE RECOVERY &middot; BATCH RUN &middot; {run_time}</div>
    <h1><span class="num">Rs {total_at_risk:,.0f}</span> across {len(rows)}<br>failed and abandoned payments.</h1>
    <p class="sub">SYNTHETIC BATCH &middot; RULE-BASED DECISIONS &middot; FULL AUDIT TRAIL BELOW</p>
  </div>
  <div class="scroll-hint">SCROLL ↓</div>
</div>

<div class="beat">
  <div class="inner">
    <div class="eyebrow">WHAT THE AGENT DID</div>
    <h1>Each transaction was diagnosed<br>against a fixed set of rules.</h1>
    <div class="stat-trio">
      <div><div class="n">{retried_count}</div><div class="l">RETRIED</div></div>
      <div><div class="n">{nudged_count}</div><div class="l">NUDGED</div></div>
      <div><div class="n">{escalated_count}</div><div class="l">ESCALATED TO HUMAN</div></div>
    </div>
  </div>
</div>

<div class="beat">
  <div class="inner">
    <div class="eyebrow">RESULT</div>
    <h1><span class="accent num">Rs {total_recovered:,.0f}</span> recovered.</h1>
    <p class="sub">{recovery_rate:.1f}% RECOVERY RATE &middot; {messaged_count} CUSTOMERS MESSAGED DIRECTLY</p>
  </div>
</div>

<div class="beat">
  <div class="inner">
    <div class="eyebrow">BOUNDS</div>
    <h1>{escalated_count} transactions were <span class="accent">not</span><br>retried or messaged automatically.</h1>
    <p class="sub">A HARD CAP ON RETRY ATTEMPTS STOPPED THE AGENT<br>FROM ACTING PAST ITS SET LIMIT</p>
  </div>
</div>

<div class="ledger-section">
  <h2>FULL AUDIT TRAIL — {len(rows)} TRANSACTIONS</h2>
  <table>
    <thead>
      <tr>
        <th>Txn</th>
        <th>Customer</th>
        <th class="num">Amount</th>
        <th>Failure</th>
        <th>Action</th>
        <th>Outcome</th>
        <th class="num">Recovered</th>
      </tr>
    </thead>
    <tbody>
      {rows_html}
    </tbody>
  </table>
</div>

<script>
  const observer = new IntersectionObserver((entries) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('shown');
      }}
    }});
  }}, {{ threshold: 0.4 }});

  document.querySelectorAll('.beat .inner').forEach(el => observer.observe(el));
</script>

</body>
</html>"""

with open("dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Dashboard saved to dashboard.html — open it in your browser.")