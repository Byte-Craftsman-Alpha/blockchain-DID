# Blockchain Based Decentralized Identity (DID)

Decentralized Identiry refers to an ID that can be used to in various fields like -
- **Authentication**: Users can login to multiple services just by using their DID instead of credentials. 
- **Identity Verification**: DID can be used to verify the credentials without exposing other information.
- **Data Portability**: DID can be used to transfer the credential between other services and plateforms seamlessly.

## Start API server
```bash
uvicorn app:app --reload
```

## How user will create their DID?

To create DID user need to send their credentials to our server through API and our server will return them a unique `DID` that can be used for the services explained above.
> `credential_oobject`
```json
{
    "user": "John D Morgan",
    "credential": {
        "personal_detail": {
            "name": {
                "first_name": "John",
                "middle_name": "D",
                "last_name": "Morgan",
                "full_name": "John D Morgan",
            },
            "parents": {
                "father_name": "Aidrew D Morgan",
                "mother_name": "Jenshy Nalia",
            },
            "dob": {
                "full": "May 11, 1974",
                "day": "Saturday",
                "date": 11,
                "month": 5,
                "year": 1974,
                "age": 50
            },
            "address": {
                "full": "138, Watsan Apartment, California, United States",
            },
            "contact": {
                "email": "johndoe8337@gmail.com",
                "contact": "+1(866) 4336 8",
                "whatsapp": "+1(866) 4336 8",
            },
        },
        "usernames": {
            "facebook.com": "john_doe_facebook",
            "instagram.com": "john_doe_insta",
            "github.com": "developer_john",
            "gmail.com": "johndoe8337",
            "domain.com": "username",
        },
        "security_credentials": {
            "facebook.com": "john_doe_facebook@face19740511$securityKey",
            "instagram.com": "john_doe_insta@inst19740511$securityKey",
            "github.com": "developer_john@gith19740511$securityKey",
            "gmail.com": "johndoe8337@gmai19740511$securityKey",
            "domain.com": "username@doma19740511$securityKey",
        },
        "other_credentials": {
            "credential_id": {
                "credential": "secret_credential",
                "access_permission": "everyone",
            },
            "credential_id": {
                "credential": "secret_credential",
                "access_permission": "everyone",
            }
        }

    }
}
```

> `API request`
```bash
curl --data '<CREDENTIALS>' <SERVER_ADDRESS>
```
`DID` will be a unique key of 16 alphanumeric characters 


Each when there will be a transaction with the credentials, a `hash` will be created and send to USER to track the shared credentials between the service provider and the DID server.

> `3e5a3ce73d13028be26be466eaa249c9abf0dd68f1a962b597763be7c5b5f20a`

## Approach
> `transactionPlay.py`
```python
import sqlite3
import blockChainAlgo
from datetime import datetime

# save transaction and generate hash
def preserveTransaction(data: object):
    """
    use your credential to create hash code
    this will also save the transaction into database for further access
    """
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("CREATE TABLE IF NOT EXISTs TRANSACTIONS (HASH, SERVER, ACCESSED_CREDENTIAL, DATE, TIME)")

    node = blockChainAlgo.Blockchain()
    node.add_block(data=data)
    hash = node.create_genesis_block().hash
    curs.execute("INSERT INTO TRANSACTIONS (HASH, SERVER, ACCESSED_CREDENTIAL, DATE, TIME) VALUES (?, ?, ?, ?, ?)", (hash, "google.com", "name, dob, contact", datetime.now().strftime("%d-%m-%Y"), datetime.now().strftime("%H:%M:%S")))
    db.commit()
    return hash

# return whole records with matching hash
def getTransaction(hash: str):
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("SELECT * FROM TRANSACTIONS WHERE HASH = ?", (hash, ))
    return curs.fetchall()

def getTransactionList():
    db = sqlite3.connect("transaction_record.db")
    curs = db.cursor()
    curs.execute("SELECT * FROM TRANSACTIONS")
    return curs.fetchall()
```
> `blockChainAlgo.py`
```python
import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.now().isoformat(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), datetime.now().isoformat(), data, latest_block.hash)
        self.chain.append(new_block)
```
> `mongoBD.py`
```python
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, uri="mongodb://localhost:27017/", database_name="test_db"):
        """
        Initialize the MongoDB connection.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        print(f"Connected to MongoDB database: {database_name}")

    def insert_data(self, collection_name, data):
        """
        Insert a single document or multiple documents into a collection.
        """
        collection = self.db[collection_name]
        if isinstance(data, list):
            result = collection.insert_many(data)
            return result.inserted_ids
        else:
            result = collection.insert_one(data)
            return result.inserted_id

    def update_data(self, collection_name, filter_criteria, update_values, update_one=True):
        """
        Update document(s) in a collection.
        """
        collection = self.db[collection_name]
        if update_one:
            result = collection.update_one(filter_criteria, {"$set": update_values})
            return result.modified_count
        else:
            result = collection.update_many(filter_criteria, {"$set": update_values})
            return result.modified_count

    def fetch_data(self, collection_name, filter_criteria=None, projection=None):
        """
        Fetch document(s) from a collection.
        """
        collection = self.db[collection_name]
        if filter_criteria is None:
            filter_criteria = {}
        documents = collection.find(filter_criteria, projection)
        return list(documents)

    def delete_data(self, collection_name, filter_criteria, delete_one=True):
        """
        Delete document(s) from a collection.
        """
        collection = self.db[collection_name]
        if delete_one:
            result = collection.delete_one(filter_criteria)
            return result.deleted_count
        else:
            result = collection.delete_many(filter_criteria)
            return result.deleted_count

    def drop_collection(self, collection_name):
        """
        Drop a collection from the database.
        """
        collection = self.db[collection_name]
        collection.drop()
        print(f"Collection '{collection_name}' dropped.")

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
        print("MongoDB connection closed.")
```

## Documentation and Tutorial
> Generate View of your Transactions
```javascript
var url = "http://127.0.0.1:8000/view_transaction/";

var data = {
    AuthID: "10012025013947uEKIeKlmFYx1nNct", // Your Auth key
};

// Making the POST request
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse the JSON response
    })
    .then(result => {
        console.log("Server Response:", result); // Handle the result
    })
    .catch(error => {
        console.error("Error:", error); // Handle any errors
    });
``` 
> Generate your Auth Key
```javascript
var url = "http://127.0.0.1:8000/generate_token/";

var data = {
    user : "John D Morgan",
    credential : {
        personal_detail : {
            name : {
                first_name : "John",
                middle_name : "D",
                last_name : "Morgan",
                full_name : "John D Morgan",
            },
            parents : {
                father_name : "Aidrew D Morgan",
                mother_name : "Jenshy Nalia",
            },
            dob : {
                full : "May 11, 1974",
                day : "Saturday",
                date : 11,
                month : 5,
                year : 1974,
                age : 50
            },
            address : {
                full : "138, Watsan Apartment, California, United States",
            },
            contact : {
                email : "johndoe8337@gmail.com",
                contact : "+1(866) 4336 8",
                whatsapp : "+1(866) 4336 8",
            },
        },
        usernames : {
            "facebook.com" : "john_doe_facebook",
            "instagram.com" : "john_doe_insta",
            "github.com" : "developer_john",
            "gmail.com" : "johndoe8337",
            "domain.com" : "username",
        },
        security_credentials : {
            "facebook.com" : "john_doe_facebook@face19740511$securityKey",
            "instagram.com" : "john_doe_insta@inst19740511$securityKey",
            "github.com" : "developer_john@gith19740511$securityKey",
            "gmail.com" : "johndoe8337@gmai19740511$securityKey",
            "domain.com" : "username@doma19740511$securityKey",
        },
        other_credentials : {
            credential_id : {
                credential : "secret_credential",
                access_permission : "everyone",
            },
            credential_id : {
                credential : "secret_credential",
                access_permission : "everyone",
            }
        }
        
    }
}

// Making the POST request
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json" 
    },
    body: JSON.stringify(data)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse the JSON response
    })
    .then(result => {
        console.table(result); // Handle the result
    })
    .catch(error => {
        console.error("Error:", error); // Handle any errors
    });

```

> View Hash Info
```javascript
var url = "http://127.0.0.1:8000/view_property/hash";

var data = {
    hash: "4eeac8f4b0c07c3405367733c5441b8d3b4d81812d05794da0cfba922f17dce7",
     // Your HASH key
};

// Making the POST request
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse the JSON response
    })
    .then(result => {
        console.table(result); // Handle the result
    })
    .catch(error => {
        console.error("Error:", error); // Handle any errors
    });
```

> Request for Credentials
```javascript
var url = "http://127.0.0.1:8000/getCredentials";

var data = {
    AuthID: "10012025013947uEKIeKlmFYx1nNct", // Your HASH key
    credentials: ["name", "contact", "email"], // What credentials you need?
};

// Making the POST request
fetch(url, {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
})
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse the JSON response
    })
    .then(result => {
        console.log("Server Response:", result); // Handle the result
    })
    .catch(error => {
        console.error("Error:", error); // Handle any errors
    });
```