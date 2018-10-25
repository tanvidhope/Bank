from django.contrib.auth.models import User
from django import forms
from django.forms import PasswordInput

from accounts.models import Profile, Transaction


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('balance',)


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['receiver', 'amount']
