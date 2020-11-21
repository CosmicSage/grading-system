from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm

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

def register(request):
    # print(dir(request), request.path, request.get_raw_uri(), request.headers)
    import json
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        print(f"{dir(form)}\n\n, {form.data},\n\n{dir(form.hidden_fields)}\n\n{dir(form.errors)}\n\n{form.full_clean}\n\n{form.error_messages}")
        if form.is_valid():
            pass
        else:
            context = dict(message=form.error_messages)
            return HttpResponseRedirect(reverse('account', args=(form.data["type"][0].lower()[0],)))

        # try:
        #     if request.body["type"].lower()[0] in ['s', 't']:
        #         print(request.body)
        # except (KeyError, IndexError) as e:
        #     return CustomHttpResponse(code=409)
        # print(request.body)
        return HttpResponse(json.dumps(dict(go="bo")), content_type="application/json")
    return CustomHttpResponse(code=405)

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
