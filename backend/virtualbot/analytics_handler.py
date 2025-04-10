# analytics_handler.py
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv
load_dotenv()

text_analytics_endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
text_analytics_key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")

credential = AzureKeyCredential(text_analytics_key)
client = TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=credential)

def analyze_health_text(text):
    """Extract health entities from text"""
    try:
        # Use healthcare-specific analysis
        response = client.analyze_healthcare_entities([text])[0]
        
        # Extract useful entities with categories
        extracted_entities = []
        for entity in response.entities:
            extracted_entities.append({
                "text": entity.text,
                "category": entity.category,
                "confidence_score": entity.confidence_score
            })
        
        # Identify relationships between entities
        relations = []
        for relation in response.entity_relations:
            relations.append({
                "relation_type": relation.relation_type,
                "source": relation.source.text,
                "target": relation.target.text
            })
            
        return {
            "entities": extracted_entities,
            "relations": relations
        }
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return {"entities": [], "relations": []}

def extract_medical_conditions(text):
    """Focus on just getting medical conditions"""
    results = analyze_health_text(text)
    conditions = [entity for entity in results["entities"] 
                 if entity["category"] == "SymptomOrSign" or 
                    entity["category"] == "Diagnosis"]
    return conditions