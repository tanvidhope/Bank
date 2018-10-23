from django.urls import path

from . import views

urlpatterns = [
    path('', views.index , name='login'), # send to login form
    # path('home/', name='home'), # go to this after login
    # path('transaction/', name='transaction'), # for transaction, maybe
     path('register/', views.UserFormView.as_view(), name='register'),
]