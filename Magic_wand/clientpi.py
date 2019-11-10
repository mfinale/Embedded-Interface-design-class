import boto3

# Let's use Amazon S3
sqs = boto3.resource('sqs')
polly = boto3.client('polly')
for queue in sqs.queues.all():
    print(queue.url)
response = polly.synthesize_speech(VoiceId='Joanna', OutputFormat='mp3',  Text = 'This is a sample text to be synthesized.')

file = open('speech.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()
print ("fuck you")