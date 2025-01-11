from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

class MongoDBHandler:
    def __init__(self, uri="mongodb://localhost:27017/", database_name="test_db"):
        """
        Initialize the MongoDB connection.
        """
        self.client = MongoClient(uri)
        self.db = self.client[database_name]
        print(f"Connected to MongoDB database: {database_name}")

    def create_unique_index(self, collection_name, field_name):
        """
        Create a unique index for a specific field in a collection.
        """
        collection = self.db[collection_name]
        result = collection.create_index([(field_name, 1)], unique=True)
        print(f"Unique index created for field '{field_name}' in collection '{collection_name}'. Index name: {result}")

    def fetch_credentials_by_keys(self,keys_to_search: list, collection_name, filter_criteria=None):
        """
        Fetch documents and search for specific keys, including in nested dictionaries.
        """
        def extract_keys(document, keys):
            """
            Recursively search for keys in a document (including nested).
            """
            result = {key: None for key in keys}  # Initialize with None
            stack = [(document, key) for key in keys]  # Stack for DFS
            
            while stack:
                current, key_to_find = stack.pop()
                if isinstance(current, dict):
                    # Check if the key exists at the current level
                    if key_to_find in current:
                        result[key_to_find] = current[key_to_find]
                    else:
                        # Push children to the stack for further exploration
                        stack.extend([(value, key_to_find) for value in current.values() if isinstance(value, (dict, list))])
                elif isinstance(current, list):
                    # Handle list elements
                    stack.extend([(element, key_to_find) for element in current if isinstance(element, (dict, list))])
            return result
        
        # Fetch documents based on filter_criteria
        collection = self.db[collection_name]
        try:
            if filter_criteria is None:
                filter_criteria = {}
            documents = list(collection.find(filter_criteria))
            
            # Extract requested keys from each document
            results = []
            for doc in documents:
                result = extract_keys(doc, keys_to_search)
                results.append(result)
            return results
        
        except Exception as e:
            print(f"Error while fetching credentials by keys: {e}")
            return []

    def insert_data(self, collection_name, data):
        """
        Insert a single document or multiple documents into a collection with duplicate prevention.
        """
        collection = self.db[collection_name]
        try:
            if isinstance(data, list):
                result = collection.insert_many(data, ordered=False)  # `ordered=False` skips duplicates
                return result.inserted_ids
            else:
                result = collection.insert_one(data)
                return result.inserted_id
        except DuplicateKeyError as e:
            print(f"Duplicate entry detected: {e}")
            return None

    def update_data(self, collection_name, filter_criteria, update_values, update_one=True):
        """
        Update document(s) in a collection.
        """
        collection = self.db[collection_name]
        try:
            if update_one:
                result = collection.update_one(filter_criteria, {"$set": update_values})
            else:
                result = collection.update_many(filter_criteria, {"$set": update_values})
            return result.modified_count
        except Exception as e:
            print(f"Error while updating: {e}")
            return 0

    def fetch_data(self, collection_name, filter_criteria=None, projection=None):
        """
        Fetch document(s) from a collection.
        """
        collection = self.db[collection_name]
        try:
            if filter_criteria is None:
                filter_criteria = {}
            documents = collection.find(filter_criteria, projection)
            return list(documents)
        except Exception as e:
            print(f"Error while fetching data: {e}")
            return []

    def delete_data(self, collection_name, filter_criteria, delete_one=True):
        """
        Delete document(s) from a collection.
        """
        collection = self.db[collection_name]
        try:
            if delete_one:
                result = collection.delete_one(filter_criteria)
            else:
                result = collection.delete_many(filter_criteria)
            return result.deleted_count
        except Exception as e:
            print(f"Error while deleting: {e}")
            return 0

    def drop_collection(self, collection_name):
        """
        Drop a collection from the database.
        """
        try:
            collection = self.db[collection_name]
            collection.drop()
            print(f"Collection '{collection_name}' dropped.")
        except Exception as e:
            print(f"Error while dropping collection: {e}")

    def close_connection(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()
        print("MongoDB connection closed.")
