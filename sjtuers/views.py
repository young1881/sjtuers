from django.http import HttpResponseRedirect


def index_view(request):
    return HttpResponseRedirect('/index/')