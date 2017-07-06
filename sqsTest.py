conf = {
   "sqs-access-key": "AKIAJUYQR43YRT6APTJQ",
   "sqs-secret-key": "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",
   "sqs-queue -name": "Temperature",
   "sqs-region": "us-east-1",
   "sqs-path": "sqssend"
}

import boto.sqs
import os
import glob
import time

conn = boto.sqs.connect_to_region(conf.get('sqs-region'),
                                  aws_access_key_id = conf.get('sqs-access-key'),
                                  aws_secret_access_key = conf.get('sqs-secret-key')
                                  )
q = conn.create_queue(conf.get('sqs-queue-name'))
from boto.sqs.message import RawMessage

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
   q.write(read_temp())
   print(read_temp())
   time.sleep(1)
