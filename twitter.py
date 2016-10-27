import json

from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
from elasticsearch import Elasticsearch

es = Elasticsearch(['https://search-twittmap-pehb35byikz6e5x5vompvtdjbm.us-west-2.es.amazonaws.com'])

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
                    res = es.index(index="twitter", doc_type='tweets', body=doc)
                    #with open("twitter_data.json",'a') as f:
                    #    f.write("\n" + '{ "index" : { "_index" : "twitter", "_type" : "tweets" } }')
                    #    f.write("\n" + '{"id": \"' + str(tweet["id"]) + '\","text": \"' + tweet["created_at"] + '\", "text": \"' + tweet["text"] + '\", "lon": \"' + str(tweet["coordinates"]['coordinates'][0]) + '\", "lat": \"' + str(tweet["coordinates"]['coordinates'][0]) + '\"}')
                    print("Added to elasticsearch" + doc)
        except:
            pass

oauth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
oauth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET)
twitterStream = Stream(oauth,PublicStreamListner())
twitterStream.filter(track=['trump','hillary','clinton','election','new','united','states','new','york','and','from'])
