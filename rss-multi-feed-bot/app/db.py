import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS rss_tracker (
            id SERIAL PRIMARY KEY,
            feed_url TEXT UNIQUE NOT NULL,
            last_guid TEXT
        )
    """)
    await conn.close()

async def get_last_guid(feed_url):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow(
        "SELECT last_guid FROM rss_tracker WHERE feed_url=$1",
        feed_url
    )
    await conn.close()
    return row["last_guid"] if row else None

async def save_last_guid(feed_url, guid):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(
        """
        INSERT INTO rss_tracker (feed_url, last_guid)
        VALUES ($1, $2)
        ON CONFLICT (feed_url)
        DO UPDATE SET last_guid = $2
        """,
        feed_url, guid
    )
    await conn.close()
