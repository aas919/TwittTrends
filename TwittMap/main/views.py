from django.shortcuts import render
from elasticsearch import Elasticsearch

import json

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
    return render(request, 'main/marker.html', {'data': data,'hits':len(hits)})    