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
    allow = offset
    dont_allow = ''
    if '+not+' in offset:
        [allow, dont_allow] = offset.split('+not+')
    s= ''
    for word in allow.split('+'):
        s+= "&allowedIngredient[]=%s" % (word)
    for word in dont_allow.split('+'):
        s+= "&excludeIngredient[]=%s" % (word)
    url = 'http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s%s&requirePictures=true' % (APP_ID, APP_KEY, s)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    result = json.loads(page)
    results = []

    for re in result['matches']:
        re['smallImageUrls'] = [re['smallImageUrls'][0].replace('.s.', '.l.')]
        name = re['recipeName']
        if len(name)>40:
            name = name[:37]+"..."
        re['recipeName'] = name
        results.append(re)
    return render_to_response("search.html", {
    'search_results' : results, 'term': offset.replace('+', ', ').title(),
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
    youtube = ''
    try:
        youtube_URL = "http://query.yahooapis.com/v1/public/yql?q=select%20%2A%20from%20youtube.search%20where%20query%3D%22"+"cooking "+str(name)+"%22%20limit%201&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
        you_res = mechanize.urlopen(youtube_URL)
        youpage = ''.join(str(line) for line in you_res)
        youres  = json.loads(youpage)

        if youres['query']['count'] > 0:
            youtube = youres['query']['results']['video']['id']
    except:
        pass

    answers = ''
    try:
        answers_URL = "http://query.yahooapis.com/v1/public/yql?q=select%20%2A%20from%20answers.search%20where%20query%3D%22"+ str(name) +"%22%20and%20type%3D%22resolved%22%20limit%204&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback="
        ans_res = mechanize.urlopen(answers_URL)
        anspage = ''.join(str(line) for line in ans_res)
        ansres  = json.loads(anspage)

        if ansres['query']['count'] > 0:
            answers = ansres['query']['results']['Question']
    except:
        pass

    return render_to_response("cook.html",{
        'flavors': results['flavors'], 'ingredients': results['ingredientLines'], 'name': results['name'], 'rating': results['rating'], 'serves': results['numberOfServings'],
            'source': results['source'], 'type': results['attributes'], 'estimated': results['totalTimeInSeconds'], 'image': results['images'][0]['hostedLargeUrl'],
             'youtube': youtube, 'nutrition': results['nutritionEstimates'], 'answers': answers,
        }, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response("thanks.html", {
        }, context_instance = RequestContext(request))


def help(request):
    return render_to_response("home.html", {
        'err': 'Please search below and select a recipe to see how to cook!',
        }, context_instance = RequestContext(request))

def recommend(request):
    return render_to_response("recommend.html", {
        }, context_instance = RequestContext(request))
