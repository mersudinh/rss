import asyncio
from app.config import CHECK_INTERVAL_MINUTES, RSS_FEEDS
from app.rss_parser import fetch_and_parse_rss
from app.webhook import send_to_webhook
from app.db import get_last_guid, save_last_guid
import os

WEBHOOK_URLS = os.getenv("WEBHOOK_URLS", "")
WEBHOOK_URLS = [u.strip() for u in WEBHOOK_URLS.split(",") if u.strip()]


async def check_feeds_once():
    print("[Scheduler] Checking feeds...", flush=True)

    for feed_url in RSS_FEEDS:
        last_guid = await get_last_guid(feed_url)
        posts = await fetch_and_parse_rss(feed_url)

        if not posts:
            print(f"[Scheduler] Feed empty: {feed_url}", flush=True)
            continue

        new_posts = []
        for post in posts:
            if last_guid and post["guid"] == last_guid:
                break
            new_posts.append(post)

        new_posts.reverse()

        for post in new_posts:
            for hook in WEBHOOK_URLS:
                print(f"[Scheduler] Sending → {post['title']}", flush=True)
                await send_to_webhook(hook, post)

        if posts:
            latest_guid = posts[0]["guid"]
            await save_last_guid(feed_url, latest_guid)


def start_scheduler():
    async def scheduler_loop():
        while True:
            try:
                await check_feeds_once()
            except Exception as e:
                print("[Scheduler Error]", e, flush=True)
            await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)

    loop = asyncio.get_event_loop()
    loop.create_task(scheduler_loop())
    print("[Scheduler] Started", flush=True)
