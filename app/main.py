from fastapi import FastAPI
from app.config import RSS_FEEDS
from app.rss_parser import fetch_and_parse_rss
from app.webhook import send_to_webhook
from app.db import init_db, get_last_guid, save_last_guid
import os

app = FastAPI()

# Multiple webhook support: CSV in Railway ENV var
WEBHOOK_URLS = os.getenv("WEBHOOK_URLS", "")
WEBHOOK_URLS = [u.strip() for u in WEBHOOK_URLS.split(",") if u.strip()]


@app.on_event("startup")
async def startup():
    await init_db()


@app.get("/")
def root():
    return {"status": "running"}


@app.get("/run")
async def run_all_feeds():
    results = []

    for feed_url in RSS_FEEDS:
        last_guid = await get_last_guid(feed_url)
        posts = await fetch_and_parse_rss(feed_url)

        if not posts:
            results.append({"feed": feed_url, "error": "feed empty or unreadable"})
            continue

        # Newest → oldest check
        new_posts = []
        for post in posts:
            if last_guid and post["guid"] == last_guid:
                break
            new_posts.append(post)

        # Feed may be old→new; reverse ensures sending oldest new item first
        new_posts.reverse()

        sent_logs = []
        for post in new_posts:
            for hook in WEBHOOK_URLS:
                ok = await send_to_webhook(hook, post)
                sent_logs.append({
                    "title": post["title"],
                    "hook": hook,
                    "sent": ok
                })

        # Save latest seen GUID
        latest_guid = posts[0]["guid"]
        await save_last_guid(feed_url, latest_guid)

        results.append({
            "feed": feed_url,
            "new_count": len(new_posts),
            "sent": sent_logs
        })

    return results
