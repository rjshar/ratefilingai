from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import json
import os
import re

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', str(text).lower()).strip('-')

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse("""<meta http-equiv='refresh' content='0; URL=/groups' />""")

@app.get("/groups", response_class=HTMLResponse)
async def groups_view(request: Request):
    df = pd.read_csv("data/cleaned_marketshare_groups.csv")
    df = df.rename(columns={
        "Market Share (%) 2024": "Market Share 2024",
        "Direct Premiums Written ($000) 2024": "Direct Premium Written",
    })
    df["Slug"] = df["Entity *"].apply(slugify)
    df = df.sort_values("2024 Rank")
    return templates.TemplateResponse("groups.html", {"request": request, "groups": df.to_dict(orient="records")})

@app.get("/group/{slug}", response_class=HTMLResponse)
async def group_detail(request: Request, slug: str):
    with open("data/parsed_filings.json") as f:
        filings_by_group = json.load(f)

    df_entity = pd.read_csv("data/cleaned_marketshare_entities.csv")
    df_entity["Group Slug"] = df_entity["Group Name"].apply(slugify)

    for group_name, filings in filings_by_group.items():
        if slugify(group_name) == slug:
            entity_marketshare = df_entity[df_entity["Group Slug"] == slug]
            return templates.TemplateResponse("entity.html", {
                "request": request,
                "group": group_name,
                "latest_filing": filings.get("latest_filing"),
                "filing_history": filings.get("filing_history", []),
                "entity_marketshare": entity_marketshare.to_dict(orient="records")
            })

    return HTMLResponse("{\"detail\":\"Group not found\"}", status_code=404)
