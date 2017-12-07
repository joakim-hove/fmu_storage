# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from django.views import View
from django.http import JsonResponse, HttpResponse


def make_url(key, kwargs, doc):
    url = reverse(key , kwargs = kwargs)
    for k,v in kwargs.iteritems():
        url = url.replace(str(v),"{%s}" % k)

    return key, url, doc

class ApiUrls(View):

    def get(self, request):
        url_list = [ make_url("api.ensemble.get_or_create", {}, "Doc"),
                     make_url("api.ensemble.add_simulation", {"ens_id" :  9999}, "Doc"),
                     make_url("api.ensemble.info", {"ens_id" : 9999}, "Doc"),
                     make_url("api.simulation.summary.data", {"id" : 9999}, "Doc"),
                     make_url("api.simulation.parameters", {"id" : 9999}, "Doc")]

        urls = { key : (url,doc) for key,url,doc in url_list }
        return JsonResponse(urls)
