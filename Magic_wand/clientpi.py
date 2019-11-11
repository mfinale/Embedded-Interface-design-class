import boto3
import time



polly = boto3.client('polly')
s3 = boto3.resource('s3')
transcribe = boto3.client('transcribe')



def text_to_speech (text):
    response = polly.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3',  Text = text)
    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()

def speech_to_text(audio_file_name):
    s3.Object('magic-wand-bucket', audio_file_name).delete()
    s3.Object('magic-wand-bucket', audio_file_name).upload_file(Filename=audio_file_name)
    job_name = "my_job"
    job_uri = "https://magic-wand-bucket.s3.amazonaws.com/"+audio_file_name
    transcribe.delete_transcription_job(TranscriptionJobName=job_name)
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
        print("Not ready yet...")
        time.sleep(5)
    print(status)



text_to_speech('Hello there. What is up?')
speech_to_text('speech.mp3')
print ("done")