import aiohttp
import xml.etree.ElementTree as ET

async def fetch_and_parse_rss(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            xml = await res.text()

    root = ET.fromstring(xml)
    items = root.findall(".//item")

    posts = []
    for item in items:
        posts.append({
            "title": item.findtext("title", "").strip(),
            "summary": item.findtext("description", "").strip(),
            "link": item.findtext("link", "").strip(),
            "guid": item.findtext("guid") or item.findtext("link")
        })

    return posts
