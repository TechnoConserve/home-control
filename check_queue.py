#!/home/pi/venv/home_control/bin/python

import boto3
import datetime
import json
import os
import psutil
import subprocess
import time

start = datetime.time(7, 00)
end = datetime.time(21, 30)

ACCESS_KEY = os.environ.get('ACCESS_KEY', '')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET', '')
REGION = 'us-east-1'
QUEUE_URL = os.environ.get('QUEUE_URL', '')

PARTY_FILE = '/home/pi/lights/party.json'


def alter_party(state):
    with open(PARTY_FILE, 'w') as f:
        data = json.load(f)
        data['party'] = state
        json.dumps(data, f)


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
            subprocess.call(['/home/pi/controls/snake_on.py'])
        elif message == "main_off":
            subprocess.call(['/home/pi/controls/snake_off.py'])
        elif message == "secondary_on":
            subprocess.call(['/home/pi/controls/red_on.py'])
        elif message == "secondary_off":
            subprocess.call(['/home/pi/controls/red_off.py'])
        elif message == 'party_on':
            now = datetime.datetime.now().time()

            if start <= now <= end:
                already_running = False
                # Don't start a new process if one is already running
                for proc in psutil.process_iter(attrs=['name']):
                    if proc.name() == 'whoshome.py':
                        already_running = True
                        break
                if not already_running:
                    subprocess.call(['/home/pi/lights/whoshome.py'])
            else:
                alter_party(1)
        elif message == 'party_off':
            alter_party(0)
            for proc in psutil.process_iter(attrs=['name']):
                if proc.name() == 'whoshome.py':
                    proc.terminate()
        elif message == 'more_red1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'red', '1', 'up'])
        elif message == 'more_green1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'green', '1', 'up'])
        elif message == 'more_blue1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'blue', '1', 'up'])
        elif message == 'less_red1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'red', '1', 'down'])
        elif message == 'less_green1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'green', '1', 'down'])
        elif message == 'less_blue1':
            subprocess.call(['/home/pi/controls/set_colors.py', 'blue', '1', 'down'])
        elif message == 'more_red2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'red', '2', 'up'])
        elif message == 'more_green2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'green', '2', 'up'])
        elif message == 'more_blue2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'blue', '2', 'up'])
        elif message == 'less_red2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'red', '2', 'down'])
        elif message == 'less_green2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'green', '2', 'down'])
        elif message == 'less_blue2':
            subprocess.call(['/home/pi/controls/set_colors.py', 'blue', '2', 'down'])
    except:
        pass
