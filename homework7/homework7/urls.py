from django.conf.urls import patterns, include, url
from views import mainpage, insert_collection, query, upload_file, list_results

""" urls.py: specifies which functions in views.py to call when certain webpages are accessed """

urlpatterns = patterns('',
    (r'^$', mainpage),
    (r'^mainpage\.html$', mainpage),
    (r'^insert_collection\.html$', insert_collection),
    (r'^upload_file\.html$', upload_file),
    (r'^query\.html$', query),
    (r'^list_results\.html$', list_results)
   )
