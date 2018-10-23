from django.contrib import admin

# Register your models here.
from accounts.models import Profile, Transaction

admin.site.register(Profile)
admin.site.register(Transaction)