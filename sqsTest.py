import boto3
import os
import glob
import time

#Connect to a session
session = Session(aws_access_key_id='AKIAJUYQR43YRT6APTJQ', aws_secret_access_key='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')

#Connect to a resource
sqs= session.resource('sqs')

queue = sqs.get_queue_by_name(QueueName=Temperature)
print(queue.url)

# Create a new message
print 'creating new message'
toWrite = 'hello world'
response = queue.send_message(MessageBody=toWrite)
print(response.get('MessageId'))

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
      temp_f = temp_c * 9.0 / 5.0 + 32.0
      return temp_c, temp_f

while True:
   print(read_temp())
   time.sleep(1)
