from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages

from main_app.models import Account

def login(request):
    print('7777777777')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect("signup")     #TODO
        else:
            messages.info(request, 'invalid username or password')
            return redirect("login")
    else:
        return render(request, 'Sign-in.html')

def sign_up(request):

    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username = username).exists():
            messages.info(request, 'username taken')
            return redirect('signup')
        elif User.objects.filter(email = email).exists():
            messages.info(request, 'email taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name = name.split()[0], last_name = name.split()[-1] , username = username, password = password, email = email)
            account = Account.objects.create(user = user, storage = 0)
            account.save()
            return redirect('login')
    else:
        return render(request, 'Sign-up.html')

