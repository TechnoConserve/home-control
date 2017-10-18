import boto3
import os

ACCESS_KEY = os.environ.get('ACCESS_KEY', '')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET', '')
REGION = 'us-west-2'
QUEUE_URL = os.environ.get('QUEUE_URL', '')


def post_message(client, message_body, url):
    response = client.send_message(QueueUrl=url, MessageBody=message_body)


def pop_message(client, url):
    response = client.receive_message(QueueUrl=url, MaxNumberOfMessages=10)

    # Last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl=url, ReceiptHandle=receipt)
    return message


client = boto3.client('sqs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=ACCESS_SECRET, region_name=REGION)
post_message(client, "test", QUEUE_URL)
message = pop_message(client, QUEUE_URL)
print(message)
