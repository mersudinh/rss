# app/config.py

# --- RSS Feed URLs ---
# Add as many as you want
RSS_FEEDS = [
    "https://example.com/feed.xml",
    "https://another.com/rss"
]

# --- Where to POST new articles ---
# Your Zapier, Make.com, LeadConnector, or custom webhook URLs
WEBHOOK_URLS = [
    "https://hooks.zapier.com/hooks/catch/xxxxxx/yyyyyy",
    "https://another-webhook.com/post"
]

# --- Scheduler: how often to check feeds (in minutes) ---
CHECK_INTERVAL_MINUTES = 10
