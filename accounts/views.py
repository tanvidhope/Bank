from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views.generic.base import View

from .forms import UserForm, ProfileForm


# Create your views here.


def index(request):
    return HttpResponse("<h1> Test1</h1>")

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'profile_form': profile_form
    })



class UserFormView(View):
    form_class = UserForm
    template_name = 'registerationForm.html'

    # display blank form
    def get(self):
        form = self.form_class(None)
        return render(self, self.template_name, {'form' : form})

    # process form data
    def post(self):
        form = self.form_class(request.POST)
        if form.is_valid():
            # make a user object of the form data, but dont put it in database yet
            user = form.save(commit=False)

            #clean the data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns user object if credentials are correct
            user = authenticate(username,password)
            if user is not None:
                login(request,user)
                balance = request.user.balance
                return HttpResponse("your balance is {% ")

        return render(self, self.template_name, {'form': form})

