from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data = request.POST)
        if form.is_valid():
            new_user = form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            # return HttpResponseRedirect('/index/')
            return render(request, 'learning_logs/index.html')
    
    context = {'form':form}
    return render(request, 'users/register.html',context)
