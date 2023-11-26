from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse

from ticketmaster import views
from ticketmaster.views import ticketmaster
from .forms import loginAccountForm, createAccountForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def login(request):

    if request.method == 'LOGOUT':
        logout_view(request)
    # Create a form instance and populate it with data from the request if request is a POST (request.POST parts works)
    # if not, create an empty form instance (None parts works below)
    form = loginAccountForm(request.POST or None)
    # Check to see if request is a POST
    # if this is a POST request, we need to process the form data and save the data
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        # before saving check whether the form data is valid:
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(reverse('ticketmaster-index'))
            # process the data in form.cleaned_data as required
            # print (form.cleaned_data['email']) # for example,email can be accessed using form.cleaned_data['email']

            # return render(request, 'ticketmaster/index.html')
        else:
            form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'login/login-page.html', context)


def create_account(request):
    form = createAccountForm(request.POST or None)
    # Check to see if request is a POST
    # if this is a POST request, we need to process the form data and save the data
    if request.method == 'POST':
        # before saving check whether the form data is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # print (form.cleaned_data['email']) # for example,email can be accessed using form.cleaned_data['email']
            form.save()
            # redirect to a new URL:
            return redirect(reverse('ticketmaster-index'))
    context = {'form': form}
    return render(request, 'login/create-account-page.html', context)


def logout_view(request):
    logout(request)