import json
import os
import logging
import urllib3

# Initializing a logger and setting it to INFO
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Reading environment variables and generating a Telegram Bot API URL
TOKEN = os.environ['TOKEN']
USER_ID = os.environ['USER_ID']
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)

http = urllib3.PoolManager()

# Helper function to prettify the message if it's in JSON
def process_message(input):
    try:
        # Loading JSON into a string
        raw_json = json.loads(input)
        # Outputing as JSON with indents
        output = json.dumps(raw_json, indent=4)
    except:
        output = input
    return output

# Main Lambda handler
def lambda_handler(event, context):
    logger.info("event=")
    logger.info(json.dumps(event))

    try:
        message = process_message(event['Records'][0]['Sns']['Message'])

        payload = json.dumps({
            "text": message,
            "chat_id": USER_ID
        })

        http.request(
            'POST',
            TELEGRAM_URL,
            headers={'Content-Type': 'application/json'},
            body=payload
        )

    except Exception as e:
        raise e