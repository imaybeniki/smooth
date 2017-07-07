import boto3
import os
import glob
import time
from boto3.session import Session
 
# Create the Boto3 Session
session = Session(
    aws_access_key_id='AKIAJUYQR43YRT6APTJQ',
    aws_secret_access_key='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',
    region_name='us-east-1',
)
client = session.client('sqs')

# Get the Queue URL
response = client.get_queue_url(
    QueueName='Temperature' 
)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
   f = open(device_file, 'r')
   lines = f.readlines()
   f.close()
   return lines

def read_temp():
   lines =read_temp_raw()
   while lines[0].strip()[-3:] != 'YES':
      time.sleep(0.2)
      lines = read_temp_raw()
   equals_pos = lines[1].find('t=')
   if equals_pos != -1:
      temp_string = lines[1][equals_pos+2:]
      temp_c = float(temp_string) / 1000.0
      return temp_c

def temp_far():
	temp_f = read_temp() * 9.0 / 5.0 + 32.0
	return temp_f

while True:
   print('C: ' + str(read_temp()) + ' F: ' + str(temp_far()))
   message = 'C: ' + str(read_temp()) + ' F: ' + str(temp_far())
   response = client.send_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/258476513244/Temperature',
    MessageBody=message,
    DelaySeconds=0,
   )
   print("Sent to AWS SQS")
   time.sleep(5)
   
   
