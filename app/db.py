import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
conn = None

async def init_db():
    global conn
    print("DEBUG_DATABASE_URL =", DATABASE_URL, flush=True)

    conn = await asyncpg.connect(DATABASE_URL)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS feed_state (
            feed_url TEXT PRIMARY KEY,
            last_guid TEXT
        )
    """)

async def get_last_guid(feed_url):
    row = await conn.fetchrow(
        "SELECT last_guid FROM feed_state WHERE feed_url=$1", feed_url
    )
    return row["last_guid"] if row else None

async def save_last_guid(feed_url, guid):
    await conn.execute("""
        INSERT INTO feed_state (feed_url, last_guid)
        VALUES ($1, $2)
        ON CONFLICT (feed_url)
        DO UPDATE SET last_guid = EXCLUDED.last_guid
    """, feed_url, guid)
