from django.contrib.auth.models import User
from django import forms
from django.forms import PasswordInput

from accounts.models import Profile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)
    balance = forms.IntegerField()

    class Meta:
        model = User
        fields = ('username', 'password','balance')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('balance',)

