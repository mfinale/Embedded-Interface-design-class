# EID Project3:
## Author: Michael Finale
## Installation Instructions
- Perform installation from project 1
- Install paho-mqtt: `pip3 install paho-mqtt`
- Clone repo from https://github.com/mfinale/Embedded-Interface-design-class.git
- Create an iot thing
- C1reate an aws rule to trigger lambda from iot thing
- Copy and paste code in lambda_code.py into lambda function
- Ensure lambda function  has AmazonSQSFullAccess and AWSLambdaSNSPublishPolicyExecutionRole permissions attached to its role 
- Create a sns topic
- Make a subscription to the sns topic for your cellphone or email
- Create a fifo sqs queue titled "Sensordata.fifo" with Content-based duplication enabled
- To give web page access to SQS queue, create a cognito identification pool and obtain cognito credentials.
- Attach  AmazonSQSFullAccess policy to cognito role using IAM.
- Grant SQS access to cognito role by assigning the appropriate policies via IAM.
- Ensure the proper credentials are defined in client_project3.html, lamda_code.py, and DHT22_application.py.
- Run `python3 DHT22_application.py` from the raspberrypi command line.


## Summary of Operation
- Raspberry pi communicates with aws iot thing via mqtt.
- These messages are routesd to lambda via a "rule" for the iot thing
- Lambda parses the messages. If it is an alert, it publishes the alert message 
to a defined sns topic. An email account that is also subscribed to this sns topic, 
received the message via email
- Otherwise, Lambda sends all sensor readings to the sqs queue with Message Group Id= sensorreadgroupid.
- A web page, with the proper credentials retrieves and deletes these readings from the SQS queue 
by using the aws sdk for javascript along with jquery.


## Project Work
Application developed by Michael Finale.  


## Project Additions
 - The web page is able to request the remaining number of records in the SQS queue.
 - The remaining number of records in the SQS queue is displayed after each transaction.

## Project Issues 
 - The "Get ALL SQS records." button currently is capable of retrieving up to 20 records from the queue. 
   Back to back requests of the sqs queue causes errors.

## References
- [1] https://gist.github.com/skirdey/9cdead881799a47742ff3cd296d06cc1
- [2] https://aws.amazon.com/blogs/iot/how-to-implement-mqtt-with-tls-client-authentication-on-port-443-from-client-devices-python/
- [3] https://mkdev.me/en/posts/how-to-send-sms-messages-with-aws-lambda-sns-and-python-3
- [4] https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html
- [5] https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html#sending-messages
- [6] https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/getting-started-browser.html
