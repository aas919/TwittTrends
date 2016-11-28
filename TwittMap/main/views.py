from django.shortcuts import render
from elasticsearch import Elasticsearch
from django.http.response import HttpResponse

import json
import boto3
from django.views.decorators.csrf import csrf_exempt

client = boto3.client('sns', region_name='us-east-1', aws_access_key_id='AKIAJOFZBQO3W3O2SDBQ', aws_secret_access_key='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')

def search_tweets(keyword):
    es = Elasticsearch(['https://search-twittmap-pehb35byikz6e5x5vompvtdjbm.us-west-2.es.amazonaws.com'], request_timeout=600)
    res = es.search(index="twitter", doc_type="tweets", size=1000, body={"query": {"term": {"text" : keyword}}})
    return res['hits']['hits']

    # Create your views here.
def render_markermap(request):
    keyword = request.GET.get("keyword")
    data = []
    hits = []
    if keyword != None:
        hits = search_tweets(keyword)
        data = '['
        for hit in hits:
            data += "{lat:" + str(hit["_source"]["lat"]) +","
            data += "lng:" + str(hit["_source"]["lon"]) + "}," 
        data += ']'
        data = data.replace(",]", "]")
    es = Elasticsearch(['https://search-twittmap-pehb35byikz6e5x5vompvtdjbm.us-west-2.es.amazonaws.com'], request_timeout=600)
    res = es.search(index='twitter', doc_type='tweets', body={"query": {"match_all": {}}})
    tweets_count = res['hits']['total']   
    return render(request, 'main/marker.html', {'data': data,'hits':len(hits), 'tweets_count':tweets_count})    

@csrf_exempt
def subscribtion_endpoint(request):
    if request.method == 'GET':
        response = client.subscribe(
            TopicArn='arn:aws:sns:us-east-1:950596917281:twittmap',
            Protocol='http',
            Endpoint='http://twittmap.cyvng2hvmf.us-west-2.elasticbeanstalk.com/subscribtion_endpoint'
        )
        print(response)
    elif request.method == 'POST':
        message_type = request.META['HTTP_X_AMZ_SNS_MESSAGE_TYPE']
        builder = json.loads(request.body.decode())
        if message_type == 'SubscriptionConfirmation':
            token = builder['Token']
            response = client.confirm_subscription(
                TopicArn='arn:aws:sns:us-east-1:950596917281:twittmap',
                Token=token,
                AuthenticateOnUnsubscribe='true'
            )
        elif message_type == 'Notification':
            message = builder['Message']
            es = Elasticsearch(['https://search-twittmap-pehb35byikz6e5x5vompvtdjbm.us-west-2.es.amazonaws.com'], request_timeout=600)
            doc = {
                'msg': json.loads(message)
            }
            es.index(index='twitter', doc_type='tweets', body=json.loads(message))
    return HttpResponse('OK')
