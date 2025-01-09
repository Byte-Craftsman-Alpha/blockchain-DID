from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.person_database
collection = db.person_collection

# Insert a person document
person_data = {
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
# collection.insert_one(person_data)

# Retrieve data by name
result = collection.find_one({"credential.personal_detail.name.full_name": "John D Morgan"})
print(result)