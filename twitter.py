import json
import certifi
import boto3
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from elasticsearch import Elasticsearch

sqs = boto3.resource('sqs')
#queue = sqs.create_queue(QueueName='twittmap', Attributes={'DelaySeconds': '5'})
#print(queue.url)
#print(queue.attributes.get('DelaySeconds'))

ACCESS_TOKEN = '784933573031624705-j29j5R9k0qTqrbtpbATPjbiwVv8gjII'
ACCESS_SECRET = 'GnurE7EOP7mKE93RfApDj5gqSGEZ0NDfnZu9zVyQXytZf'
CONSUMER_KEY = 'kcExHNk6xa9lLPHFXmCGnsUfJ'
CONSUMER_SECRET = '80mgMi8AmJ8KSZmOEE8aAM3ajDRiNeNmx5txIYJCyz4NX6IB77'

class PublicStreamListner(StreamListener):

    def on_data(self, raw_data):
        try:
            tweet = json.loads(raw_data)
            if('coordinates' in tweet):
                if tweet["coordinates"] is not None:
                    doc = {
                        'id' : tweet["id"],
                        'created_at' : tweet["created_at"],
                        'lon' : tweet["coordinates"]['coordinates'][0],
                        'lat' : tweet["coordinates"]['coordinates'][1],
                        'text' : tweet["text"]
                        }
                    queue = sqs.get_queue_by_name(QueueName='twittmap')
                    response = queue.send_message(MessageBody=json.dumps(doc))
                    print(response.get('MessageId'))
        except:
            pass

oauth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
twitterStream = Stream(oauth,PublicStreamListner())
twitterStream.filter(track=['trump','hillary','clinton','election','new','united','states','new','york','and','from'])
