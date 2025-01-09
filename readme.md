# Blockchain Based Decentralized Identity (DID)

Decentralized Identiry refers to an ID that can be used to in various fields like -
- **Authentication**: Users can login to multiple services just by using their DID instead of credentials. 
- **Identity Verification**: DID can be used to verify the credentials without exposing other information.
- **Data Portability**: DID can be used to transfer the credential between other services and plateforms seamlessly.

## How user will create their DID?

To create DID user need to send their credentials to our server through API and our server will return them a unique `DID` that can be used for the services explained above.
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
```bash
curl --data '<CREDENTIALS>' <SERVER_ADDRESS>
```
`DID` will be a unique key of 16 alphanumeric characters 


Each when there will be a transaction with the credentials, a `hash` will be created and send to USER to track the shared credentials between the service provider and the DID server.
```
3e5a3ce73d13028be26be466eaa249c9abf0dd68f1a962b597763be7c5b5f20a
```
