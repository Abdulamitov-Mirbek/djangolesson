from http.client import HTTPResponse

from django.shortcuts import render
def home(request):
    return HTTPResponse( "server run like new")
# Create your views here.
