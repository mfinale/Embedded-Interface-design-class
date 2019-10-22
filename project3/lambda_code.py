# Python 3 code that is ran on lambda in aws.
# Code runs on event defined by trigger in aws.
# Handler parses JSON message from trigger and sends to SNS if it is an alert and/or
# sends it to a SQS queue.
# sSns topic and sqs url must be defined.


import json
from botocore.exceptions import ClientError
import urllib
import boto3
import logging

print('Loading function')



def lambda_handler(event, context):
    print("Label = " + event['Label'])
    if (event['Label']=="Alert"):
        print("Timestamp = " + str(event['Timestamp']))
        print("Temperature Alert Level = " + str(event['Temperature Alert Level']))
        print("Temperature Trigger Level = " + str(event['Temperature Trigger Level']))
        print("Humidity Alert Level = " + str(event['Humidity Alert Level']))
        print("Humidity Trigger Level = " + str(event['Humidity Trigger Level']))
        sns = boto3.client('sns')
        sns.publish(
            TopicArn="arn:aws:sns:us-east-1:374381767834:sensor_sns",
            Subject="Sensor Alert",
            Message=json.dumps(event)
            )
        print ('Sent a message to an Amazon SNS topic.')
    elif (event['Label']=="sensor_read"):
        sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/374381767834/Sensordata.fifo'
        sqs_client = boto3.client('sqs')
        msg_body =  json.dumps(event)
        msg_id = "sensorreadgroupid"
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url, MessageBody=msg_body,  MessageGroupId= msg_id)
        print("Timestamp = " + str(event['Timestamp']))
        print("Temperature = " + str(event['Temperature']))
        print("Humidity = " + str(event['Humidity']))
        print ('Sent a message to an Amazon SQS queue.')
    