from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . forms import SignUpForm

# Create your views here.
def memberLogin(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(request,username=username, password=password)
			if user is not None:
				login(request,user)
				return redirect('home')
			else:
				messages.success(request,('There is an error login. Try again'))
				return redirect('login')
			
		else:
			return render(request,'authenticate/login.html')
	else:
		return redirect('home')


def memberSignup(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			form = SignUpForm(request.POST)
			if form.is_valid():
				messages.success(request, 'Congratulations! You havbe become an Author!')
				form.save()
				return redirect('login')
		else:
			form = SignUpForm()
		return render(request, 'authenticate/signup.html', {'form': form})
	else:
		return redirect('home')

def memberLogout(request):
	logout(request)
	messages.warning(request,'Logout Successfully!!')
	return redirect('login')