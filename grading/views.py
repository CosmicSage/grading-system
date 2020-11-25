from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from .models import Account, Assignment, Responder

# Create your views here.
def index(request):
    context = dict()
    if request.user.is_authenticated:
        # Get User's account
        account = Account.objects.get(user=request.user)
        context.update(dict(account=account))
    return render(request, "grading/index.html", context)

def login(request):
    message = None
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse("home"))
                else:
                    message = "Invalid username or password"
            except KeyError:
                return CustomHttpResponse(code=411)
        else:
            message = "Invalid username or password"
    context = dict(
        form=AuthenticationForm,
        message=message
    )

    return render(request, "grading/login.html", context)

def assignments(request):
    if request.method == "POST":
        # Potentially dangerous
        # REVIEW:
        try:
            # get the guy's account
            account = Account.objects.get(user=request.user)

        except Account.DoesNotExist:
            return CustomHttpResponse(code=402)

        if account.is_student:
            try:
                # Get the code now
                code = request.POST.get('code')

                # get the guy's reponder avatar
                responder = Responder.objects.get(student=account)

                # get the assignment
                assignment = Assignment.objects.get(code=code)

                # If assign exists, add the guy to the assignment
                assignment.responders.add(responder)

                return HttpResponseRedirect(reverse("assignments"))

            except (Assignment.DoesNotExist, KeyError, Responder.DoesNotExist):
                return CustomHttpResponse(code=402)

        elif account.is_teacher:
            try:
                title = request.POST.get("title")
                desc = request.POST.get("description")
                a = Assignment(title=title, description=desc)
                a.save()
                a.teacher.add(account)
            except KeyError:
                return CustomHttpResponse(code=403)
            HttpResponseRedirect(reverse("assignments"))
    context = dict()
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        if account.is_teacher:
            # Get all assignments created by this teacher
            work = account.grader.all()
            context.update(dict(is_teacher=True))

        elif account.is_student:
            # Get the guy
            responder = Responder.objects.get(student=account)

            # Get all assignments this guy signed up for
            work = responder.volunteer.all()
            context.update(is_student=True)
        else:
            CustomHttpResponse(code=412)
        context.update(dict(work=work))
        return render(request, "grading/assignments.html", context)
    return CustomHttpResponse(code=401)

def a(request, a_code):
    return HttpResponse(f"{Assignment.objects.get(code=a_code)}")

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("home"))

def account(request, type):
    # print(dir(request), f"\n\n{request.content_params}", f"\n\n{request._messages}")
    if type not in ['s', 't']:
        return CustomHttpResponse(code=511)
    context = dict(
        type="Student" if type == "s" else "Teacher",
        form=UserCreationForm,
        message=[x.message for x in messages.get_messages(request)]
    )
    return render(request, "grading/register.html", context)

def register(request):
    # print(dir(request), request.path, request.get_raw_uri(), request.headers)
    import json
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        try:
            type = form.data["type"][0].lower()[0]
        except KeyError:
            return CustomHttpResponse(code=406)
        # print(f"{dir(form)}\n\n, {form.data},\n\n{dir(form.hidden_fields)}\n\n{dir(form.errors)}\n\n{form.full_clean}\n\n{form.error_messages}")

        if form.is_valid() and type in ['s', 't']:
            # Everthin alright log em in
            print("alrririttyyyy")

            # Create user
            user = form.save()

            # Link user with account
            account = Account(user=user, is_student=True if type == 's' else False, is_teacher=True if type == 't' else False)
            account.save()

            # Additional Statement to fix model logic bug may remove in future
            if type == 's':
                # Create a Responder
                responder = Responder(student=account)
                responder.save()

            # auto-Login post registration
            auth_login(request, user)
            return HttpResponseRedirect(reverse("home"))

        else:
            messages.add_message(request, messages.ERROR, f"{form.error_messages}")
            return HttpResponseRedirect(reverse('account', args=(type,)))

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
