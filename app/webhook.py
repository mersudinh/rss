import aiohttp
from html import unescape
from html.parser import HTMLParser

HTTP_TIMEOUT = aiohttp.ClientTimeout(total=15)


class _HTMLTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self._chunks = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self._chunks.append(text)

    def text(self):
        return " ".join(self._chunks)


def _html_to_text(html):
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return unescape(parser.text())


async def _fetch_html(session, url):
    if not url:
        return ""
    try:
        async with session.get(url, timeout=HTTP_TIMEOUT) as res:
            if res.status != 200:
                return ""
            return await res.text()
    except Exception:
        return ""

async def send_to_webhook(url, item):
    async with aiohttp.ClientSession() as session:
        html = await _fetch_html(session, item.get("link", ""))
        content = _html_to_text(html) if html else ""
        payload = {
            "Title": item["title"],
            "Summary": item["summary"],
            "Link": item["link"],
            "Content": content,
        }

        print(f"[DEBUG] Sending webhook to {url}", flush=True)
        print(f"[DEBUG] Payload = {payload}", flush=True)

        try:
            async with session.post(url, json=payload, timeout=HTTP_TIMEOUT) as res:
                print(f"[DEBUG] Webhook status: {res.status}", flush=True)
                return res.status in [200, 201, 202]
        except Exception as e:
            print("[DEBUG] Webhook error:", e, flush=True)
            return False
