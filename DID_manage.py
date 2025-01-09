import sqlite3

def initialize_db():
    conn = sqlite3.connect("dids.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS DIDs (
            id TEXT PRIMARY KEY,
            public_key TEXT NOT NULL,
            blockchain_address TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_did(did, public_key, blockchain_address):
    conn = sqlite3.connect("dids.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO DIDs (id, public_key, blockchain_address) VALUES (?, ?, ?)", 
                   (did, public_key, blockchain_address))
    conn.commit()
    conn.close()
