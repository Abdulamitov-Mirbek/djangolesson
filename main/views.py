from http.client import HTTPResponse

from django.shortcuts import render
def home(request):
    return HTTPResponse( "server run")
# Create your views here.
