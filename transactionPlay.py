import sqlite3
import blockChainAlgo
from datetime import datetime
import random
from pydantic import BaseModel
import string

def generateDID():
    now = datetime.now()
    characters = string.ascii_letters + string.digits  # Letters (lowercase and uppercase) and digits
    return ''.join(now.strftime("%d%m%Y%H%M%S").split() + [random.choice(characters) for _ in range(16)])

# save transaction and generate hash
def preserveTransaction(data: object, user: str):
    """
    use your credential to create hash code
    this will also save the transaction into database for further access
    """
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTs TRANSACTIONS (USER, HASH, SERVER, ACCESSED_CREDENTIAL, DATE, TIME)")

    node = blockChainAlgo.Blockchain()
    node.add_block(data=data)
    hash = node.create_genesis_block().hash
    curs.execute("INSERT INTO TRANSACTIONS (USER, HASH, SERVER, ACCESSED_CREDENTIAL, DATE, TIME) VALUES (?, ?, ?, ?, ?, ?)", (user, hash, data.requestingServer, str(list(data.credentials.keys())), datetime.now().strftime("%d-%m-%Y"), datetime.now().strftime("%H:%M:%S")))
    db.commit()
    return hash

# return whole records with matching hash
def getTransaction(hash: str):
    """
    get the information about transaction through hash key
    """
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("SELECT * FROM TRANSACTIONS WHERE HASH = ?", (hash, ))
    return curs.fetchall()

def getTransactionList(user: str):
    """
    get list of all transaction from any user and any hash key
    """
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("SELECT * FROM TRANSACTIONS WHERE USER = ?", (user, ))
    return curs.fetchall()

def getTranscationInfo(hash: str):
    """
    get transaction information through hash key
    """
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("SELECT * FROM TRANSACTIONS WHERE HASH = ?", (hash, ))
    return curs.fetchall()

class demoCredential(BaseModel):
    user: str
    credential: object

class credentialRequest(BaseModel):
    AuthID: str
    credentials: list

class viewTransactionCredentials(BaseModel):
    AuthID: str

class hashProperty(BaseModel):
    hash: str
