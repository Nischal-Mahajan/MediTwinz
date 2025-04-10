# db_handler.py
from azure.cosmos import CosmosClient
import azure.cosmos.exceptions as exceptions
import datetime
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Cosmos client - CHANGE THIS PART
connection_string = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
# Extract endpoint and key from connection string
if connection_string:
    parts = connection_string.split(';')
    cosmos_uri = parts[0].replace('AccountEndpoint=', '')
    cosmos_key = parts[1].replace('AccountKey=', '')
else:
    # Fallback to separate variables if needed
    cosmos_uri = os.getenv("AZURE_COSMOS_URI")
    cosmos_key = os.getenv("AZURE_COSMOS_KEY")

client = CosmosClient(cosmos_uri, credential=cosmos_key)

# Rest of your code remains the same
database_name = "healthassistant"
conversation_container_name = "conversations"
patient_container_name = "patientdata"

database = client.get_database_client(database_name)
conversation_container = database.get_container_client(conversation_container_name)
patient_container = database.get_container_client(patient_container_name)

# Functions remain unchanged
def log_conversation(user_id, user_message, bot_response, entities=None):
    """Store conversation history in Cosmos DB"""
    try:
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()
        
        conversation_item = {
            "id": conversation_id,
            "userId": user_id,
            "userMessage": user_message,
            "botResponse": bot_response,
            "extractedEntities": entities or [],
            "timestamp": timestamp
        }
        
        conversation_container.create_item(body=conversation_item)
        return conversation_id
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error logging conversation: {e}")
        return None

def get_user_conversation_history(user_id, limit=10):
    """Retrieve conversation history for a user"""
    try:
        query = f"SELECT * FROM c WHERE c.userId = '{user_id}' ORDER BY c.timestamp DESC OFFSET 0 LIMIT {limit}"
        items = list(conversation_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return items
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error retrieving conversation history: {e}")
        return []

def save_patient_data(patient_id, data):
    """Store or update patient information"""
    try:
        # Check if patient record exists
        query = f"SELECT * FROM c WHERE c.patientId = '{patient_id}'"
        existing_items = list(patient_container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        
        if existing_items:
            # Update existing record
            item = existing_items[0]
            item.update(data)
            patient_container.replace_item(item=item['id'], body=item)
            return item['id']
        else:
            # Create new record
            data["id"] = str(uuid.uuid4())
            data["patientId"] = patient_id
            data["createdAt"] = datetime.datetime.utcnow().isoformat()
            patient_container.create_item(body=data)
            return data["id"]
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error saving patient data: {e}")
        return None