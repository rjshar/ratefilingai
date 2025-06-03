from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.filters["slugify"] = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-') if isinstance(s, str) else ""

# Load group-level data
group_df = pd.read_csv("data/cleaned_marketshare_groups.csv")
group_df.rename(columns={
    "2024 Rank": "Rank",
    "Entity *": "Group",
    "Market Share (%) 2024": "Share 2024",
    "Market Share (%) 2023": "Share 2023",
    "Market Share (%) 2022": "Share 2022",
    "Direct Premiums Written ($000) 2024": "Premium 2024",
    "Direct Premiums Written ($000) 2023": "Premium 2023",
    "Direct Premiums Written ($000) 2022": "Premium 2022"
}, inplace=True)

for col in ["Share 2024", "Share 2023", "Share 2022", "Premium 2024", "Premium 2023", "Premium 2022"]:
    group_df[col] = group_df[col].fillna(0)

industry_total = {
    "Rank": "-",
    "Group": "Total Industry",
    "Share 2024": 100.0,
    "Share 2023": 100.0,
    "Share 2022": 100.0,
    "Premium 2024": group_df["Premium 2024"].sum(),
    "Premium 2023": group_df["Premium 2023"].sum(),
    "Premium 2022": group_df["Premium 2022"].sum()
}
group_records = [industry_total] + group_df.sort_values(by="Rank").to_dict(orient="records")

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/groups")

@app.get("/groups", response_class=HTMLResponse)
async def group_listing(request: Request):
    return templates.TemplateResponse("groups.html", {
        "request": request,
        "groups": group_records
    })

def slugify(text):
    if not isinstance(text, str):
        return ""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

# Entity-level data
entity_df = pd.read_csv("data/cleaned_marketshare_entities.csv")
entity_df.rename(columns={"Entity *": "Entity Name"}, inplace=True)

def parse_float(val):
    try:
        return float(val)
    except:
        return 0.0

entity_df["Direct Premiums Written ($000) 2024"] = entity_df["Direct Premiums Written ($000) 2024"].apply(parse_float)
entity_df["Market Share (%) 2024"] = entity_df["Market Share (%) 2024"].apply(parse_float)
entity_df["Adjusted Loss Ratio (%) 2024"] = entity_df["Adjusted Loss Ratio (%) 2024"].apply(parse_float)

@app.get("/group/{slug}", response_class=HTMLResponse)
async def group_detail(slug: str, request: Request):
    matched_group = None
    for group_name in group_df["Group"].dropna().unique():
        if slugify(group_name) == slug:
            matched_group = group_name
            break

    if not matched_group:
        raise HTTPException(status_code=404, detail="Group not found")

    group_entities = entity_df[entity_df["Group"] == matched_group]

    return templates.TemplateResponse("entity.html", {
        "request": request,
        "group_name": matched_group,
        "entities": group_entities.to_dict(orient="records")
    })
