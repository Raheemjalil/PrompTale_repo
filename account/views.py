from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.template import loader
from django.http import JsonResponse
from account.forms import RegistrationForm, AccountAuthenticationForm
from .models import Account
from django.db import IntegrityError
from django.contrib import messages

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)

def logout_view(request):
	logout(request)
	return redirect('home')

def login_view(request):
	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)

def update_view(request): 
	return render(request, 'account/update.html', {})

def update_record(request, username):
	errors = ""
	user = request.POST['username']
	email = request.POST['email']

	member = Account.objects.get(username=username)
	if user != member.username and Account.objects.filter(username=user).exists():
		errors += "username/" + user
	if email != member.email and Account.objects.filter(email=email).exists():
		errors += " email/" + email
	try:
		member.username = user
		member.email = email
		member.save()
	except IntegrityError as e:
			messages.error(request, errors)
			return redirect("update")	
	
	return redirect("home")

def create_story(request):
	return render(request, 'account/create.html', {})

def my_stories(request):
	return render(request, 'account/stories.html', {})
