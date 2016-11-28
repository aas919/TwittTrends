import boto3
import json
from watson_developer_cloud import AlchemyLanguageV1
from jsonmerge import merge

alchemy_language = AlchemyLanguageV1(api_key='a478af3840b5d6cef311a1b6dbab00ce879e03d3')

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='twittmap')

client = boto3.client('sns')

while True:
    # Process messages by printing out body
    for message in queue.receive_messages(MaxNumberOfMessages=10):
        # Print out the body
        try:
            tweet = json.loads(message.body)
            notification_message = merge(tweet, alchemy_language.sentiment(text=tweet['text'])['docSentiment'])
            response = client.publish(
                TopicArn='arn:aws:sns:us-east-1:950596917281:twittmap',
                Message=json.dumps(notification_message),
                Subject='New Tweet'
                )
            print(response)
        except:
            pass
        # Let the queue know that the message is processed
        message.delete()
