from django.contrib import admin
from .models import Account, Assignment, Responder

# Register your models here.
admin.site.register(Account)
admin.site.register(Responder)
admin.site.register(Assignment)
