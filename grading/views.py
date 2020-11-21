from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm

from http import HTTPStatus
from django.http import HttpResponse

# class code():
#     def __init__(self, code):
#         super(code, self).__init__()
#         self.arg = arg

class CustomHttpResponse(HttpResponse):
    """docstring for CustomHttpResponse."""

    def __init__(self, **kwargs):
        super(CustomHttpResponse, self).__init__()
        error = HTTPStatus(kwargs["code"])
        self.content = F"<h2>{error.value}</h2><h1>{error.phrase}</h1><hr>"
        self.status_code = error.value


# class CustomHttpResponse(HttpResponse, code):
#     def someRandomFunction(self, code):
#         error = HTTPStatus(code)
#         self.message = error.phrase
#         self.status_code = error.value

# class HttpResponseNoContent(HttpResponse):
#     status_code = HTTPStatus.NO_CONTENT

# Create your views here.
def index(request):
    return render(request, "grading/index.html")

def login(request):
    return HttpResponse("Sda")

def logout(request):
    return HttpResponse("DOSILGJAOEW")

def account(request, type):
    if type not in ['s', 't']:
        return CustomHttpResponse(code=511)
    context = dict(
        type="Student" if type == "s" else "Teacher",
        form=UserCreationForm
    )
    return render(request, "grading/register.html", context)
