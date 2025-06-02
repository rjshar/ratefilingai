from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

# 🔐 Set your password here
SECRET_PASSWORD = "insurancerules"

summaries = {
    "af group": """<h2>Accident Fund Group – MI WC Filing</h2>...""",  # keep your full HTML here
    "chubb": """<h2>Chubb Group – MI WC Filing</h2>...""",
    "travelers": """<h2>Travelers Group – MI WC Filing</h2>...""",
    "liberty": """<h2>Liberty Mutual Group – MI WC Filing</h2>...""",
    "hartford": """<h2>Hartford Group – MI WC Filing</h2>...""",
    "zurich": """<h2>Zurich Group – MI WC Filing</h2>...""",
    "caom": """<h2>CAOM – Advisory Loss Cost Filing</h2>..."""
}

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
    <body>
        <h1>RateFilingAI Demo</h1>
        <p><b>Enter group name and password to view filing summary.</b></p>
        <form action="/summary" method="post">
            Group Name: <input type="text" name="group"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Get Filing Summary">
        </form>
    </body>
    </html>
    """

@app.post("/summary", response_class=HTMLResponse)
async def summary(group: str = Form(...), password: str = Form(...)):
    if password != SECRET_PASSWORD:
        return "<p>❌ Incorrect password. Access denied.</p>"

    key = group.lower()
    for name in summaries:
        if name in key:
            return summaries[name]
    return f"<p>No filing data available for group: {group}</p>"
