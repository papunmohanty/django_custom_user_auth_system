from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from .forms import UserRegistrationForm 

# Create your views here.
def home(request):
	return render(request, 'userauth/home.html')

def register(request):
	# return HttpResponse('Hi')
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			userObj = form.cleaned_data
			username = userObj['username']
			email = userObj['email']
			password = userObj['password']
			get_user_ip = request.get_host()
			if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
				User.objects.create_user(username, email, password)
				user = authenticate(username = username, password = password)
				login(request, user)
				return HttpResponseRedirect('/', {'get_user_ip': get_user_ip})
			else:
				forms.ValidationError('Looks like a username with that email or password already exists')
	else:
		form = UserRegistrationForm()
	return render(request, 'userauth/register.html', {'form': form})
	
