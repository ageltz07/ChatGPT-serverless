import os
import json
from urllib.parse import parse_qs
import boto3

# External api's that will be used
import openai
import json
from twilio.rest import Client


def lambda_handler(event, context):
    
    # Get my environment variables for twilio and twilio number
    twilio_sid = os.environ['TWILIO_ACCOUNT_SID']
    twilio_token = os.environ['TWILIO_AUTH_TOKEN']
    twilio_num = os.environ['TWILIO_PHONE_NUMBER']
    
    # Get environment variable holding the OpenAI key and set it
    openai_key = os.environ['OPENAI_KEY']
    openai.api_key = openai_key
    
    # Setup the twilio client and set 
    twilio_client = Client(twilio_sid, twilio_token)
    
    # Twilio sends data as x-www-form-urlencoded by default
    # so we have to parse the data first.
    twilio_data = parse_qs(event['body'])
    
    user_prompt = twilio_data['Body'][0]
    sender_number = twilio_data['From'][0]
    
    response = get_gpt_response(user_prompt)
    print(response)
    send_message(twilio_client, response, sender_number, twilio_num)
    return 'OK', 200
    
    
def send_message(twilio_client, message, recipient, twilio_num):
    twilio_client.messages.create(
        from_=twilio_num,
        body=message,
        to=recipient
    )


def get_gpt_response(msg):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages = [{'role': 'user', 'content': msg}],
    temperature=0.3,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return "ChatGPT:\n\n" + response["choices"][0]['message']['content']
