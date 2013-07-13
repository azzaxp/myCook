# mYcook views will come here

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
    s = ''
    for word in offset.split('+'):
        s+= "&allowedIngredient[]=%s" % (word)
    url = 'http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s%s&requirePictures=true' % (APP_ID, APP_KEY, s)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    result = json.loads(page)
    results = []

    for re in result['matches']:
        re['smallImageUrls'] = [re['smallImageUrls'][0].replace('.s.', '.l.')]
        results.append(re)
    return render_to_response("search.html", {
    'search_results' : results, 'term': offset.replace('+', ' ').title(),
        }, context_instance=RequestContext(request))


def where(request):
    return render_to_response("where.html", {
        }, context_instance=RequestContext(request))

def how(request, offset):
    import json
    import mechanize
    if offset == '':
        return HttpResponseRedirect('/help/')

    url = 'http://api.yummly.com/v1/api/recipe/%s?_app_id=%s&_app_key=%s' % (offset, APP_ID, APP_KEY)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    results = json.loads(page)
    name = results['name']
    youtube_URL = "http://query.yahooapis.com/v1/public/yql?q=select%20%2A%20from%20youtube.search%20where%20query%3D%22"+str(name)+"%22%20limit%201&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
    you_res = mechanize.urlopen(youtube_URL)
    youpage = ''.join(str(line) for line in you_res)
    youres  = json.loads(youpage)
    return render_to_response("cook.html",{
        'flavors': results['flavors'], 'ingredients': results['ingredientLines'], 'name': results['name'], 'rating': results['rating'], 'serves': results['numberOfServings'],
            'source': results['source'], 'type': results['attributes'], 'estimated': results['totalTimeInSeconds'], 'image': results['images'][0]['hostedLargeUrl'],
             'youtube': youres['query']['results']['video']['id']
        }, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response("thanks.html", {
        }, context_instance = RequestContext(request))


def help(request):
    return render_to_response("home.html", {
        'err': 'Please search below and select a recipe to see how to cook!',
        }, context_instance = RequestContext(request))

def recommend(request):
    return HttpResponse("Recommend something!")