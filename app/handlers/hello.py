import json
from logger import logger

def handler(event, context):
    logger.info(event)
    logger.info(context)
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "event ": event,
            "context": context
        })
    }
