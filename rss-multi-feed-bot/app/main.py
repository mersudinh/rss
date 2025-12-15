from fastapi import FastAPI
from app.config import RSS_FEEDS
from app.rss_parser import fetch_and_parse_rss
from app.webhook import send_to_webhook
from app.db import init_db, get_last_guid, save_last_guid
import os

app = FastAPI()

WEBHOOK_URL = os.getenv("WEBHOOK_URL")


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/run")
async def run_all_feeds():
    all_results = []

    for feed_url in RSS_FEEDS:
        last_guid = await get_last_guid(feed_url)
        posts = await fetch_and_parse_rss(feed_url)

        if not posts:
            all_results.append({"feed": feed_url, "error": "no posts"})
            continue

        new_posts = []
        for p in posts:
            if last_guid and p["guid"] == last_guid:
                break
            new_posts.append(p)

        new_posts.reverse()

        sent = []
        for p in new_posts:
            ok = await send_to_webhook(WEBHOOK_URL, p)
            sent.append({"title": p["title"], "sent": ok})

        latest_guid = posts[0]["guid"]
        await save_last_guid(feed_url, latest_guid)

        all_results.append({
            "feed": feed_url,
            "new_count": len(new_posts),
            "sent": sent
        })

    return all_results
