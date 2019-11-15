import boto3
import time
import urllib
import json
import pygame


# aws resources
polly = boto3.client('polly')
s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')
rekognition= boto3.client('rekognition')



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

#converts a jpeg image into bytes and sends to aws rekognition which assigns the photo a label
def get_image_label(photo):
    print ("Analyzing image using rekognition.")
    with open(photo, 'rb') as source_image:
        source_bytes = source_image.read()
        response= rekognition.detect_labels(Image={'Bytes':source_bytes}, MaxLabels=1, MinConfidence=99.0)
        response = response['Labels'][0]['Name']
        return response








#Test 1: convert given text to audio. Play the  audio file. Process audio file using AWS transcribe.
text_to_speech('Identify.')
play_audio('speech.mp3')
speech_to_text('speech.mp3')
# Test 2: Get a label for a specified image via aws rekognition. Convert label to audio. Play audio.
result = get_image_label('texas-flag-lonestar-state-usa.jpg')
print (result)
text_to_speech(result)
play_audio('speech.mp3')




print ("done")