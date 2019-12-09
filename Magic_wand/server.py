import boto3
import botocore
import time
from time import sleep
import mysql.connector
import json
from botocore.exceptions import ClientError



s3 = boto3.resource('s3')
sqs=boto3.client('sqs')
sqs_queue_url='https://sqs.us-east-1.amazonaws.com/374381767834/magicwand_queue.fifo'	
#create a databas connection
mydb = mysql.connector.connect(host="localhost",user="admin",passwd="mfeid123",
                               database='magicwanddb')
mycursor = mydb.cursor()


#start with clean table called "command_data" and "label_data"
mycursor.execute("DROP TABLE command_data")
mycursor.execute("CREATE TABLE command_data ( message_type VARCHAR(50), command VARCHAR(100), is_valid VARCHAR(20), time VARCHAR(100))")
mycursor.execute("DROP TABLE label_data")
mycursor.execute("CREATE TABLE label_data ( message_type VARCHAR(50),  image_label VARCHAR(100), result VARCHAR(20), time VARCHAR(100))")


BUCKET_NAME = 'my-bucket' # replace with your bucket name
KEY = 'my_image_in_s3.jpg' # replace with your object key

#retrieves image from magic-wand-image-bucket and saves as "capture_from_s3.jpg"
def retrieve_image():
    try:
        s3.Bucket("magic-wand-image-bucket").download_file('capture.jpg', 'capture_from_s3.jpg')
        print ("Retrieved image from s3 magic-wand-image-bucket")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")



# retrieve sqs function adopted from https://docs.aws.amazon.com/code-samples/latest/catalog/python-sqs-receive_message.py.html
def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5):
    """Retrieve messages from an SQS queue

    The retrieved messages are not deleted from the queue.

    :param sqs_queue_url: String URL of existing SQS queue
    :param num_msgs: Number of messages to retrieve (1-10)
    :param wait_time: Number of seconds to wait if no messages in queue
    :param visibility_time: Number of seconds to make retrieved messages
        hidden from subsequent retrieval requests
    :return: List of retrieved messages. If no messages are available, returned
        list is empty. If error, returns None.
    """

    # Validate number of messages to retrieve
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10

    # Retrieve messages from an SQS queue
    sqs_client = boto3.client('sqs')
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
        return msgs['Messages']
    except:
        print ("No messages in SQS queue")
        return None

    # Return the list of retrieved messages



def delete_sqs_message(sqs_queue_url, msg_receipt_handle):
    """Delete a message from an SQS queue

    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_receipt_handle: Receipt handle value of retrieved message
    """

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs')
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)


def main():
    num_messages = 1
    # Retrieve a SQS message and send to label_data table or command_data table depending on message_type
    # Delete the message from the SQS queue afterwards. Retrieve latest image from s3.
    # Do this once every 6 seconds.
    while (True):
        retrieve_image()
        msgs = retrieve_sqs_messages(sqs_queue_url, num_messages)
        if msgs is not None:
            for msg in msgs:
                data = msg["Body"]
                delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])
                #print(data)
                data = json.loads(data)
                msg_type = data["message_type"]
                if "command" in msg_type:
                    val = (data["message_type"],data["command"],data["is_valid"],data["time"])
                    sql = "INSERT INTO command_data (message_type, command, is_valid, time) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(sql, val)
                    mydb.commit()
                elif "Evaluate_label" in msg_type:
                    val = (data["message_type"],data["image_label"],data["result"],data["time"])
                    sql = "INSERT INTO label_data (message_type, image_label, result, time) VALUES (%s, %s, %s, %s)"
                    mycursor.execute(sql, val)
                    mydb.commit()
        #the below code for mysql is for checking databases
        mycursor.execute("SELECT * FROM command_data")
        myresult= mycursor.fetchall()
        for x in myresult:
            print (x)
        mycursor.execute("SELECT * FROM label_data")
        myresult= mycursor.fetchall()
        for x in myresult:
            print (x)
        #sleep 6 seconds between each iteration
        time.sleep(6)



if __name__ == '__main__':
    main()







print ("done")