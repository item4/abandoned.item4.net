from django.http.response import HttpResponse


def index(request):
    """Index page. do nothing."""

    return HttpResponse('Hello World!')
