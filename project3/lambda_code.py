import json
#from __future__ import print_function
import urllib
import boto3


print('Loading function')


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))
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
            Message=str(event)
            )
        print ('Sent a message to an Amazon SNS topic.')
    elif (event['Label']=="sensor_read"):
        print("Timestamp = " + str(event['Timestamp']))
        print("Temperature = " + str(event['Temperature']))
        print("Humidity = " + str(event['Humidity']))