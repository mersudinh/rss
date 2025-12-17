import aiohttp

async def send_to_webhook(url, item):
    payload = {
        "Title": item["title"],
        "Summary": item["summary"],
        "Link": item["link"]
    }

    print(f"[DEBUG] Sending webhook to {url}", flush=True)
    print(f"[DEBUG] Payload = {payload}", flush=True)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as res:
                print(f"[DEBUG] Webhook status: {res.status}", flush=True)
                return res.status in [200, 201, 202]
        except Exception as e:
            print("[DEBUG] Webhook error:", e, flush=True)
            return False
