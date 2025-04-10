# app_insights.py
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging
import os
from dotenv import load_dotenv
load_dotenv()

# Application Insights config
APPINSIGHTS_CONNECTION_STRING = os.getenv("APPINSIGHTS_CONNECTION_STRING")

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if APPINSIGHTS_CONNECTION_STRING:
    # Add Azure Log Handler to the logger
    logger.addHandler(
        AzureLogHandler(
            connection_string=APPINSIGHTS_CONNECTION_STRING
        )
    )

# Configure Flask middleware
def initialize_app_insights(app):
    if APPINSIGHTS_CONNECTION_STRING:
        FlaskMiddleware(
            app,
            exporter=None,
            sampler=ProbabilitySampler(rate=1.0),
            connection_string=APPINSIGHTS_CONNECTION_STRING
        )
        return True
    return False

# Helper functions
def log_request(user_id, message, response):
    """Log request details to Application Insights"""
    if APPINSIGHTS_CONNECTION_STRING:
        properties = {
            'user_id': user_id,
            'message': message,
            'response_length': len(response) if response else 0
        }
        logger.info('Chat request processed', extra={'custom_dimensions': properties})

def log_exception(user_id, error):
    """Log exceptions to Application Insights"""
    if APPINSIGHTS_CONNECTION_STRING:
        properties = {
            'user_id': user_id,
            'error': str(error)
        }
        logger.exception('Error processing request', extra={'custom_dimensions': properties})