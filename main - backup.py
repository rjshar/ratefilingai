from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import stripe
import os

app = FastAPI()

# 🔐 Basic password (still works)
SECRET_PASSWORD = "insurancerules"

# 💳 Stripe setup
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
DOMAIN = "https://ratefilingai.onrender.com"  # ← Update this if needed

summaries = {
    "af group": "<h2>Accident Fund Group – MI WC Filing</h2>...",
    "chubb": "<h2>Chubb Group – MI WC Filing</h2>...",
    "travelers": "<h2>Travelers Group – MI WC Filing</h2>...",
    "liberty": "<h2>Liberty Mutual Group – MI WC Filing</h2>...",
    "hartford": "<h2>Hartford Group – MI WC Filing</h2>...",
    "zurich": "<h2>Zurich Group – MI WC Filing</h2>...",
    "caom": "<h2>CAOM – Advisory Loss Cost Filing</h2>..."
}

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
    <body>
        <h1>RateFilingAI Demo</h1>
        <p><b>Enter group name and password:</b></p>
        <form action="/summary" method="post">
            Group Name: <input type="text" name="group"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Get Filing Summary">
        </form>
        <hr>
        <h3>Or Subscribe for Unlimited Access:</h3>
        <form action="/create-checkout-session" method="POST">
            <button type="submit">💳 Subscribe with Stripe</button>
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

@app.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': 1500,  # $15.00
                    'product_data': {
                        'name': 'RateFilingAI Access',
                        'description': 'Access to Michigan WC filing summaries'
                    },
                },
                'quantity': 1,
            }],
            success_url=f"{DOMAIN}/?success=true",
            cancel_url=f"{DOMAIN}/?canceled=true",
        )
        return RedirectResponse(url=session.url, status_code=303)
    except Exception as e:
        return HTMLResponse(f"<p>Error creating Stripe session: {e}</p>")
