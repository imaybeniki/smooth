import boto3
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


while True:
   response = client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/258476513244/Temperature',
    DelaySeconds=0,
   )
   print(response)
   time.sleep(5)
   
   
