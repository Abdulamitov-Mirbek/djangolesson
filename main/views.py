from django.http import HttpResponse

def home(request):
    return HttpResponse("Сервер работает Hello World")
