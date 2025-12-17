import asyncpg
import os

# Railway internal connection variables
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")
PGDATABASE = os.getenv("PGDATABASE")

DATABASE_URL = (
    f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
)

conn = None

async def init_db():
    global conn
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
