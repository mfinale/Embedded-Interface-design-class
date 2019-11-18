import boto3
import time
import datetime
import urllib
import json
import pygame
from botocore.exceptions import ClientError
import logging


# aws resources
polly = boto3.client('polly')
s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')
rekognition= boto3.client('rekognition')
sqs=boto3.client('sqs')
sqs_queue_url='https://sqs.us-east-1.amazonaws.com/374381767834/magicwand_queue.fifo'	


# plays specified audio file to raspberry pi speaker
def play_audio(audio_file_speaker):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_speaker)
    print("Playing audio on speaker")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue


#converts given text to an audio file titled "speech.mp3"
def text_to_speech (text):
    print ('converting text to audio')
    response = polly.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3',  Text = text)
    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

## Grabs a specified local audio file. Loads it to a aws-s3 bucket where it is then converted to text by aws-transcribe
def speech_to_text(audio_file_name):
    s3.Object('magic-wand-bucket', audio_file_name).delete()
    s3.Object('magic-wand-bucket', audio_file_name).upload_file(Filename=audio_file_name)
    job_name = "my_job"
    job_uri = "https://magic-wand-bucket.s3.amazonaws.com/"+audio_file_name
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
    print ("Beginning transciption of recorded speech.")
    play_audio('processing.mp3')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': job_uri},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Transcribing speech. Transcription Status: "+status['TranscriptionJob']['TranscriptionJobStatus'])
        time.sleep(5)
    print(status['TranscriptionJob']['TranscriptionJobStatus'])
    url=status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print ('Retrieving result from url.')
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read()
    else:
        print("Error getting transcript data", operUrl.getcode())
    data= json.loads(data)
    data = data['results']['transcripts']
    data= data[0]['transcript']
    print (data)
    return data

#converts a jpeg image into bytes and sends to aws rekognition which assigns the photo a label
def get_image_label(photo):
    print ("Analyzing image using rekognition.")
    with open(photo, 'rb') as source_image:
        source_bytes = source_image.read()
        response= rekognition.detect_labels(Image={'Bytes':source_bytes}, MaxLabels=1, MinConfidence=99.0)
        response = response['Labels'][0]['Name']
        return response

# function to evaluate voice command from user. Accepts identify, wrong, and correct. Sends all recorded commands to sqs
def command_isvalid(command_text):
    if 'identify' in command_text:
        print ('Received command ['+ command_text+ '] from user.')
        text_to_speech('Received voice command: '+ command_text)
        play_audio('speech.mp3')
        #function to take a photo
        isvalid_result = True
    elif 'wrong' in command_text:
        print ('Received command ['+ command_text+ '] from user.')
        isvalid_result = True
    elif 'correct' in command_text:
        print ('Received command ['+ command_text+ '] from user.')
        isvalid_result = True
    else:
        print ('ERROR: ['+ command_text+'] is not a valid command')
        text_to_speech('ERROR: '+ command_text+' is not a valid command')
        play_audio('speech.mp3')
        isvalid_result = False
    sqs_info = {"message_type":"voice_command","command": command_text, "is_valid":isvalid_result, "time": str(datetime.datetime.now())}
    sqs_info = json.dumps(sqs_info)
    send_to_sqs(sqs_info)
    return isvalid_result


#evaluate user's response to label that was generated for image. Send result to SQS
def evaluate_result(transcribed_user_command,label):
    if 'wrong' in transcribed_user_command:
        sqs_info = {"message_type":"Evaluate_label","image_label": label, "result":"wrong","time": str(datetime.datetime.now())}
        print ('Label for image is wrong.')
        play_audio('wrong.mp3')
    elif 'correct' in transcribed_user_command:
        sqs_info = {"message_type":"Evaluate_label","image_label": label, "result":"correct","time": str(datetime.datetime.now())}
        print ('Label for image is correct!')
        play_audio('correct.mp3')
    sqs_info = json.dumps(sqs_info)
    send_to_sqs(sqs_info)



#def function to send image to s3


#function that sends data to sqs
def send_to_sqs(msg_body):
    try:
        msg = sqs.send_message(QueueUrl=sqs_queue_url,MessageBody=msg_body,MessageGroupId='magicwand_group')
    except ClientError as e:
        logging.error(e)
        return None
    return msg




#Test 1: convert given text to audio. Play the  audio file. Process audio file using AWS transcribe.
#text_to_speech('Identify.')
#play_audio('speech.mp3')
#speech_to_text('speech.mp3')
# Test 2: Get a label for a specified image via aws rekognition. Convert label to audio. Play audio.
#result = get_image_label('texas-flag-lonestar-state-usa.jpg')
#print (result)
#text_to_speech(result)
#play_audio('speech.mp3')
# Test 3: Evaluate a string for a command transcribed from user's voice and evaluate if valid or not. (also send results to sqs)
command_text= 'wrong'
command_isvalid(command_text)
command_text= 'self destruct'
command_isvalid(command_text)
command_isvalid('identify')
#Test 4: Evaluate the response recorded by the user for given label for an image. Respond to the user with a sound and send results to SQS
evaluate_result('correct','test_label')
evaluate_result('wrong','test_label')


##mainloop pseudo code
#listen for users voice
#record audio
#transcribe audio
#evaluate transcribed audio
#if not identify - say invalid command and loop
#if identify -
#capture and store image (play audio while capturing)
#send to aws lex to get label
# play audio of label back to user and ask is this correct or wrong?
#listen for users voice
#record audio
#transcribe audio
#evaluate transcribed audio
# if not wrong or correct say invalid command and loop back
# if correct or wrong evaluate response against label
# start from beginning





print ("done")