from django.contrib import admin
from .models import SignupUser, LoginRecord

admin.site.register(SignupUser)
admin.site.register(LoginRecord)
