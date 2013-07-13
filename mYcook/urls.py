from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mYcook.views.home', name='home'),
    # url(r'^mYcook/', include('mYcook.foo.urls')),
    url(r'^ask', 'mYcook.views.ask', name='home'),
    url(r'^get/([A-Za-z+ ]*)', 'mYcook.views.get', name='home'),
    url(r'^where', 'mYcook.views.where', name='home'),
    url(r'^help', 'mYcook.views.help', name='home'),
    url(r'^enjoy', 'mYcook.views.recommend', name='home'),
    url(r'^thanks', 'mYcook.views.thanks', name='home'),
    url(r'^how/([A-Za-z0-9_\- ]*)', 'mYcook.views.how', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
