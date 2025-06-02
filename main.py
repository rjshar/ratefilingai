from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 📊 Load and format 3-year market share data
df = pd.read_csv("data/marketshare_groups.csv")

df.rename(columns={
    "2024 Rank": "Rank",
    "Entity *": "Group",
    "Market Share (%) 2024": "Share 2024",
    "Market Share (%) 2023": "Share 2023",
    "Market Share (%) 2022": "Share 2022",
    "Direct Premiums Written ($000) 2024": "Premium 2024",
    "Direct Premiums Written ($000) 2023": "Premium 2023",
    "Direct Premiums Written ($000) 2022": "Premium 2022"
}, inplace=True)

# Clean missing values
for col in ["Share 2024", "Share 2023", "Share 2022",
            "Premium 2024", "Premium 2023", "Premium 2022"]:
    df[col] = df[col].fillna(0)

# Total industry stats
industry_total = {
    "Rank": "-",
    "Group": "Total Industry",
    "Share 2024": 100.0,
    "Share 2023": 100.0,
    "Share 2022": 100.0,
    "Premium 2024": df["Premium 2024"].sum(),
    "Premium 2023": df["Premium 2023"].sum(),
    "Premium 2022": df["Premium 2022"].sum()
}

group_records = [industry_total] + df.sort_values(by="Rank").to_dict(orient="records")

@app.get("/groups", response_class=HTMLResponse)
async def group_listing(request: Request):
    return templates.TemplateResponse("groups.html", {
        "request": request,
        "groups": group_records
    })
