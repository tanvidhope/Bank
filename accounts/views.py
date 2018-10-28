from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#from django.core.checks import messages
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.views.generic.base import View

from django.core.mail import send_mail
from django.conf import settings


from .forms import UserForm, ProfileForm, TransactionForm


# Create your views here.


def index(request):
    return HttpResponse("<h1> Test1</h1>")

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            instance = request.user.profile
            bal = int(request.POST.get('balance',''))
            profile_form.save()
            request.user.profile.balance = bal
            request.user.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('home')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'profile_form': profile_form
    })


def create_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            obj, created = User.objects.get_or_create(username=request.POST.get('username'))
            if created:
                obj.set_password(request.POST.get('password'))
                obj.email = request.POST.get('email')
                obj.profile.balance = int(request.POST.get('balance',''))
                obj.save()
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect('home')
            else:
                messages.error(request, ('user already exists!'))
                return redirect('create')
        else:
            messages.error(request, ('Please correct the error below.'))
            return redirect('create')
    else:
        user_form = UserForm
        profile_form = ProfileForm
        return render(request, 'create.html', {
        'user_form': user_form,
        'profile_form': profile_form })


def make_transaction(request):
    if request.method == 'POST':
        transaction_form = TransactionForm(request.POST, instance=request.user.profile)
        if transaction_form.is_valid():
            # reciever = request.POST.get('reciever')
            if User.objects.filter(username=request.POST.get('receiver')).exists():
                amount = int(request.POST.get('amount'))
                if amount < request.user.profile.balance :
                    sender = request.user
                    request.user.profile.balance = request.user.profile.balance - amount
                    reciever = User.objects.get(username=request.POST.get('receiver'))
                    reciever.profile.balance = reciever.profile.balance + amount
                    sender.save()
                    reciever.save()
                    email_sender(amount,reciever)
                    email_reciever(amount,sender)
                    return redirect('home')
                else:
                    messages.error(request, ('Balance insufficient!'))
                    return redirect('transaction')
            else:
                messages.error(request, ('user does not exist'))
                return redirect('transaction')
    else:
        transaction_form = TransactionForm
        return render(request,'transactionForm.html',{
            'transaction_form' : transaction_form
        })


def email_sender(amt, reciever):
    subject1 = ' The money has been successfully transferred'
    message1 = ' An amount of rs ' + str(amt) +' has been sent to ' + reciever.username + '.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [reciever.email,]
    send_mail( subject1, message1, email_from, recipient_list )
    return redirect('home.html')


def email_reciever(amt, sender):
    subject = ' You have recieved money!'
    message = ' An amount of rs ' + str(amt) + ' from ' + sender.username + 'has been credited to your account.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['sender.email',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('home.html')

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
            balance = form.cleaned_data['balance']
            user.set_password(password)
            user.username = username
            user.balance = balance
            user.save()

            # returns user object if credentials are correct
            user = authenticate(username,password)
            if user is not None:
                login(request,user)
                balance = request.user.balance
                return HttpResponse("your balance is {% ")

        return render(self, self.template_name, {'form': form})


