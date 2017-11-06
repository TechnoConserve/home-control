#!/home/pi/venv/home_control/bin/python
import boto3
import os
from subprocess import call
import time

ACCESS_KEY = os.environ.get('ACCESS_KEY', '')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET', '')
REGION = 'us-east-1'
QUEUE_URL = os.environ.get('QUEUE_URL', '')


def pop_message(client, url):
    response = client.receive_message(QueueUrl=url, MaxNumberOfMessages=10)

    # last message posted becomes messages
    message = response['Messages'][0]['Body']
    receipt = response['Messages'][0]['ReceiptHandle']
    client.delete_message(QueueUrl=url, ReceiptHandle=receipt)
    return message


client = boto3.client('sqs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=ACCESS_SECRET, region_name=REGION)

waittime = 20
client.set_queue_attributes(QueueUrl=QUEUE_URL, Attributes={'ReceiveMessageWaitTimeSeconds': str(waittime)})

time_start = time.time()
while time.time() - time_start < 60:
    print("Checking...")
    try:
        message = pop_message(client, QUEUE_URL)
        print(message)
        if message == "main_on":
            call(['/home/pi/controls/snake_on.py'])
        elif message == "main_off":
            call(['/home/pi/controls/snake_off.py'])
        elif message == "secondary_on":
            call(['/home/pi/controls/red_on.py'])
        elif message == "secondary_off":
            call(['/home/pi/controls/red_off.py'])
        elif message == 'party_on':
            call(['/home/pi/lights/party.py'])
        elif message == 'party_off':
            call(['/home/pi/lights/party.py', '--state', 'off'])
        elif message == 'more_red1':
            call(['/home/pi/controls/set_colors.py', 'red', 1, 'up'])
        elif message == 'more_green1':
            call(['/home/pi/controls/set_colors.py', 'green', 1, 'up'])
        elif message == 'more_blue1':
            call(['/home/pi/controls/set_colors.py', 'blue', 1, 'up'])
        elif message == 'less_red1':
            call(['/home/pi/controls/set_colors.py', 'red', 1, 'down'])
        elif message == 'less_green1':
            call(['/home/pi/controls/set_colors.py', 'green', 1, 'down'])
        elif message == 'less_blue1':
            call(['/home/pi/controls/set_colors.py', 'blue', 1, 'down'])
        elif message == 'more_red2':
            call(['/home/pi/controls/set_colors.py', 'red', 2, 'up'])
        elif message == 'more_green2':
            call(['/home/pi/controls/set_colors.py', 'green', 2, 'up'])
        elif message == 'more_blue2':
            call(['/home/pi/controls/set_colors.py', 'blue', 2, 'up'])
        elif message == 'less_red2':
            call(['/home/pi/controls/set_colors.py', 'red', 2, 'down'])
        elif message == 'less_green2':
            call(['/home/pi/controls/set_colors.py', 'green', 2, 'down'])
        elif message == 'less_blue2':
            call(['/home/pi/controls/set_colors.py', 'blue', 2, 'down'])
    except:
        pass
