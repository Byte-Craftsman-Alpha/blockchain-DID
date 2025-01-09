from fastapi import FastAPI, HTTPException
import uuid
import sqlite3
from DID_manage import add_did, initialize_db
import blockchain

app = FastAPI()

initialize_db()

@app.post("/create_did/")
def create_did(public_key: str):
    did = f"did:blockchain:{uuid.uuid4()}"
    blockchain.Blockchain
    blockchain_address = "blockchain_address_placeholder"  # Replace with actual blockchain integration logic
    add_did(did, public_key, blockchain_address)
    return {"did": did, "blockchain_address": blockchain_address}

@app.get("/get_did/{did}")
def get_did(did: str):
    conn = sqlite3.connect("dids.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM DIDs WHERE id = ?", (did,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "public_key": row[1], "blockchain_address": row[2]}
    else:
        raise HTTPException(status_code=404, detail="DID not found")
