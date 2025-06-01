from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

summaries = {
    "af group": """
<h2>Accident Fund Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> February 1, 2024</li>
  <li><b>Overall Impact:</b> -3.0%</li>
  <li><b>Indicated Change:</b> -6.8%</li>
  <li><b>Medical Trend:</b> -3.6%</li>
  <li><b>Indemnity Trend:</b> -4.1%</li>
</ul>
<hr>
<h3>Market Share in Michigan WC (2024)</h3>
<ul>
  <li><b>Total Direct Premiums:</b> $217,410K</li>
  <li><b>Market Share:</b> 20.45%</li>
  <li><b>State Rank:</b> #1</li>
  <li><b>Top Entities:</b>
    <ul>
      <li>Accident Fund Ins Co. of Am – $89,609K (8.42%)</li>
      <li>Accident Fund National – $61,470K (5.79%)</li>
      <li>Accident Fund General – $48,267K (4.55%)</li>
    </ul>
  </li>
</ul>
""",
    "chubb": """
<h2>Chubb Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Indicated Change:</b> -9.1%</li>
  <li><b>Rate Impact:</b> +0.5%</li>
</ul>
<hr>
<p><i>Market share data not available for Chubb.</i></p>
""",
    "travelers": """
<h2>Travelers Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Indicated Change:</b> -5.2%</li>
  <li><b>Rate Impact:</b> +0.895%</li>
</ul>
<hr>
<h3>Market Share in Michigan WC (2024)</h3>
<ul>
  <li><b>Total Direct Premiums:</b> $74,007K</li>
  <li><b>Market Share:</b> 6.96%</li>
  <li><b>State Rank:</b> #2</li>
  <li><b>Top Entities:</b>
    <ul>
      <li>Travelers Indemnity Co. – $22,633K (2.13%)</li>
      <li>Charter Oak Fire – $19,728K (1.86%)</li>
      <li>Travelers Property Cas Co. – $11,518K (1.08%)</li>
    </ul>
  </li>
</ul>
""",
    "liberty": """
<h2>Liberty Mutual Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Indicated Change:</b> -1.7%</li>
  <li><b>Rate Impact:</b> +0.1%</li>
</ul>
<hr>
<h3>Market Share in Michigan WC (2024)</h3>
<ul>
  <li><b>Total Direct Premiums:</b> $44,639K</li>
  <li><b>Market Share:</b> 4.20%</li>
  <li><b>State Rank:</b> #5</li>
  <li><b>Top Entities:</b>
    <ul>
      <li>LM Insurance Corp – $13,382K (1.26%)</li>
      <li>Liberty Insurance Corp – $12,812K (1.21%)</li>
      <li>Liberty Mutual Fire – $10,743K (1.01%)</li>
    </ul>
  </li>
</ul>
""",
    "hartford": """
<h2>Hartford Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Indicated Change:</b> -6.2%</li>
  <li><b>Rate Impact:</b> 0.0%</li>
</ul>
<hr>
<h3>Market Share in Michigan WC (2024)</h3>
<ul>
  <li><b>Total Direct Premiums:</b> $54,613K</li>
  <li><b>Market Share:</b> 5.13%</li>
  <li><b>State Rank:</b> #3</li>
  <li><b>Top Entities:</b>
    <ul>
      <li>Hartford Accident & Indem Co. – $15,210K (1.43%)</li>
      <li>Trumbull Insurance Co. – $13,502K (1.27%)</li>
      <li>Twin City Fire Insurance Co. – $10,786K (1.01%)</li>
    </ul>
  </li>
</ul>
""",
    "zurich": """
<h2>Zurich Group – MI WC Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Indicated Change:</b> +1.6%</li>
  <li><b>Rate Impact:</b> +0.2%</li>
</ul>
<hr>
<h3>Market Share in Michigan WC (2024)</h3>
<ul>
  <li><b>Total Direct Premiums:</b> $46,927K</li>
  <li><b>Market Share:</b> 4.41%</li>
  <li><b>State Rank:</b> #4</li>
  <li><b>Top Entities:</b>
    <ul>
      <li>Zurich American Ins Co. – $26,308K (2.48%)</li>
      <li>American Zurich Ins Co. – $15,630K (1.47%)</li>
      <li>Fidelity & Deposit Co. of MD – $2,773K (0.26%)</li>
    </ul>
  </li>
</ul>
""",
    "caom": """
<h2>CAOM – Advisory Loss Cost Filing</h2>
<ul>
  <li><b>Effective Date:</b> January 1, 2025</li>
  <li><b>Loss Cost Level Change:</b> -3.0%</li>
</ul>
<hr>
<p><i>CAOM is an advisory bureau and does not write premium directly.</i></p>
"""
}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <body>
        <h1>RateFilingAI Demo</h1>
        <p>Try one of these companies: <b>AF Group, Chubb, Travelers, Liberty, Hartford, Zurich, CAOM</b></p>
        <form action="/summary" method="post">
            Group Name: <input type="text" name="group"><br>
            <input type="submit" value="Get Filing Summary">
        </form>
    </body>
    </html>
    """

@app.post("/summary", response_class=HTMLResponse)
async def summary(group: str = Form(...)):
    key = group.lower()
    for name in summaries:
        if name in key:
            return summaries[name]
    return f"<p>No filing data available for group: {group}</p>"
