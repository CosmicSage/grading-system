from django.contrib import admin
from .models import Account, Assignment, Response

# Register your models here.
admin.site.register(Account)
admin.site.register(Response)
admin.site.register(Assignment)
