# mYcook views will come here

import requests
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

APP_ID = '1743e444'
APP_KEY = '76a6a6be6412c439101a0c443816de27'

def home(request):
    if request.method == 'POST':
        search_key = request.POST['search_key'].strip()
        return HttpResponseRedirect('/get/%s' %(search_key.lower().replace(' ', '+')))
    else:
        return render_to_response("home.html", {
            }, context_instance=RequestContext(request))


def ask(request):
    return render_to_response("ask.html", {
        }, context_instance=RequestContext(request))


def get(request, offset):
    import mechanize
    import json

    def filter(URL):
        newURL = URL.replace(".s.jpg", ".730x410.jpg")
        resp = requests.head(newURL)
        if resp.status_code != 200:
            return URL
        return newURL

    url = 'http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&allowedIngredient[]=%s&requirePictures=true' % (APP_ID, APP_KEY, offset)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    result = json.loads(page)
    results = []

    for re in result['matches']:
        re['smallImageUrls'] = [filter(re['smallImageUrls'][0])]
        results.append(re)
    return render_to_response("search.html", {
    'search_results' : results, 'term': offset.replace('+', ' ').title(),
        }, context_instance=RequestContext(request))


def where(request):
    return render_to_response("where.html", {
        }, context_instance=RequestContext(request))

def how(request, offset):
    import mechanize
    if offset == '':
        return HttpResponseRedirect('/')

    url = 'http://api.yummly.com/v1/api/recipe/%s' % (offset)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    return render_to_response("cook.html",{
        'result': page,
        }, context_instance=RequestContext(request))