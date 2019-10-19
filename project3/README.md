# EID Project3:
## Author: Michael Finale
## Installation Instructions
- Perform installation from project 1
- install paho-mqtt:pip3 install paho-mqtt
https://docs.aws.amazon.com/iot/latest/developerguide/iot-moisture-tutorial.html
- create a iot thing
- create an aws rule tor trigger lambda from iot thing
- ensure lambda function that is running the code in lambda_code.py has AmazonSQSFullAccess 
and AWSLambdaSNSPublishPolicyExecutionRole permissions attached to its role 
- create a sns topic
- make a subscription to the sns topic for your cellphone or email
- create a fifo sqs queue titled "Sensordata.fifo" with Content-based duplication enabled
- raspberry pi communicates with aws iot thing via mqtt.
- these messages are routesd to lambda via a "rule" for the iot thing
- lambda parses the messages. If it is an alert, it publishes the alert message 
to a defined sns topic. An email account that is also subscribed to this sns topci, 
received the message via email
-All messages are sent to the sqs queue with Message Group Id= sensorreadgroupid
- and html web page interfaces with the sqs queue and retrieves data (up to 10 readings at
a time due to limitiations of Amazon SQS)

 
## Project Work
Application developed by Michael Finale.  



## Project Additions/Known Bugs
 - Retrieval of humid or temperature plots has not been implemented as of 10/6/2019 
 - Temperature conversion has been implemented for single node.js and python/tornado readings but not as part of the network responsiveness test
## References
- [1] https://gist.github.com/skirdey/9cdead881799a47742ff3cd296d06cc1
- [2] https://aws.amazon.com/blogs/iot/how-to-implement-mqtt-with-tls-client-authentication-on-port-443-from-client-devices-python/
- [3] https://mkdev.me/en/posts/how-to-send-sms-messages-with-aws-lambda-sns-and-python-3
https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html
- [4] https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html#sending-messages
