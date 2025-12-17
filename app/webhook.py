import aiohttp

async def send_to_webhook(url, item):
    payload = {
        "Title": item["title"],
        "Summary": item["summary"],
        "Link": item["link"]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as res:
            return res.status in [200, 201, 202]
