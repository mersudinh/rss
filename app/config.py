# app/config.py

# --- RSS Feed URLs ---
# Add as many as you want
RSS_FEEDS = [
    "https://www.nsf.gov/rss/rss_www_news.xml",
    "https://higheredstrategy.com/feed/",
    "https://www.higheredtoday.org/feed/",
    "https://www.highereddive.com/feeds/news/",
    "https://fsapartners.ed.gov/rss/whats-new",
    "https://agb.org/feed/",
    "https://www.msche.org/feed/",
    "https://www.hlcommission.org/feed/",
    "https://www.abhe.org/feed/",
    "https://www.wscuc.org/feed/",
    "https://www.aacc.nche.edu/feed/",
    "https://www.deac.org/feed/",
    "https://www.accsc.org/feed/",
    "https://nwccu.org/feed/",
    "https://www.higheredcompliance.org/feed/",
    "https://nc-sara.org/feed/",
    "https://upcea.edu/feed/"
]

# --- Where to POST new articles ---
# Your Zapier, Make.com, LeadConnector, or custom webhook URLs
WEBHOOK_URLS = [
    "https://services.leadconnectorhq.com/hooks/K3kCvdPAvTtR0BNoMyI9/webhook-trigger/19c214aa-defd-45a7-a118-eed96553e444"
]

# --- Scheduler: how often to check feeds (in minutes) ---
CHECK_INTERVAL_MINUTES = 60
