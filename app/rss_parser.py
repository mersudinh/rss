import aiohttp
import xml.etree.ElementTree as ET

async def fetch_and_parse_rss(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                xml = await res.text()
    except Exception:
        return []

    try:
        root = ET.fromstring(xml)
    except Exception:
        return []

    items = root.findall(".//item")

    posts = []
    for item in items:
        title = item.findtext("title", "").strip()
        summary = item.findtext("description", "").strip()
        link = item.findtext("link", "").strip()
        guid = item.findtext("guid") or link or title

        posts.append({
            "title": title,
            "summary": summary,
            "link": link,
            "guid": guid
        })

    return posts
