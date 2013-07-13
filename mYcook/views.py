# mYcook views will come here

from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

def home(request):
    return render_to_response("home.html", {
        }, context_instance=RequestContext(request))


def ask(request):
    return render_to_response("ask.html", {
        }, context_instance=RequestContext(request))