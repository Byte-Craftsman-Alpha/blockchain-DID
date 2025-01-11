from fastapi import FastAPI, Header, Request
from pydantic import BaseModel
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
from transactionPlay import *
from mongoDB import MongoDBHandler
import json

handler = MongoDBHandler()
handler.create_unique_index("credentials", "AuthID")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change to specific domains in production.
    allow_credentials=True,  # Allow cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/generate_token/") # generate Auth Key
async def generate_token(credential: demoCredential, request: Request):
    """
    Basic details extraction 
    Origin, credentials etc
    """
    Header = dict(request.headers) # Get basic information
    origin = request.headers.get("origin")

    class data: # Gather Data alon with credentials
        credentials: object = credential.credential
        requestingServer: str = str(origin)

    DID = generateDID()
    hash = preserveTransaction(data=data, user=DID)

    writeData = credential.credential
    writeData.update({"AuthID": DID})

    # Save user credential
    handler.insert_data("credentials", writeData)
    response = {"message":f"Hi {credential.user}, Your DID has been created successfuly.", "AuthID":DID, "hash_key": hash}
    return response

@app.post("/view_transaction/") # View All Transactions
async def viewTransaction(credential: viewTransactionCredentials, request: Request):
    """
    Basic details extraction 
    Origin, credentials etc
    """
    Header = dict(request.headers)
    origin = request.headers.get("origin")

    response = getTransactionList(credential.AuthID)
    return response

@app.post("/getCredentials/")  # Request for credentials
async def getCredentials(data: credentialRequest, request: Request):
    """
    This endpoint will be used to get the credential of a user.
    """
    # Extract headers
    server = request.headers.get("origin")

    # Parse request data
    AuthID = data.AuthID
    requestCredential = data.credentials

    # Create a class-like object for transaction
    class TransactionData:
        credentials = {i: "" for i in requestCredential}
        requestingServer = str(server)

    # Preserve transaction
    hash = preserveTransaction(data=TransactionData, user=AuthID)

    # Fetch credentials from database
    fetchedCredentials = handler.fetch_credentials_by_keys(
        keys_to_search=requestCredential, 
        collection_name="credentials", 
        filter_criteria={"AuthID": AuthID}
    )

    # Prepare the response
    response = {
        "message": "Request OK",
        "hash_key": hash,
        "credentials": fetchedCredentials
    }
    return response



@app.post("/view_property/hash/") # Get transaction through HASH KEY
async def hashProperty(credential: hashProperty, request: Request):
    """
    get properties of transaction through hash
    """
    Header = dict(request.headers)
    origin = request.headers.get("origin")

    hash = credential.hash
    return getTranscationInfo(hash)
