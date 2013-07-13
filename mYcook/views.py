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

    url = 'http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=%s' % (APP_ID, APP_KEY, offset)
    res = mechanize.urlopen(url)
    page = ''.join(str(line) for line in res)
    result = json.loads(page)
    return render_to_response("print.html", {
    'search_results' : result['matches'],
        }, context_instance=RequestContext(request))