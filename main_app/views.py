from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from main_app.models import Content, Library, Suffix, Category, AttachCategory, File
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from main_app.models import Account


# Create your views here.
def suffix(request):
    return render(request, 'example.html')


# def content_main_page(request, content_id):


@csrf_protect
def create_suffix(request):
    if request.method == 'POST':
        suffix_ = Suffix.objects.create(title=request.POST['suffix'])
        suffix_.save()
        return HttpResponse("Suffix has been successfully created")
    else:
        raise Http404("Request must be post")


def attach_category(request):
    return render(request, 'example2.html')


def create_attach_category(request):
    if request.method == 'POST':
        suffix_ = get_object_or_404(Suffix, pk=request.POST['suffix-id'])
        attach_category = AttachCategory.objects.create(title=request.POST['title'])
        attach_category.allowed_suffixes.add(suffix_)
        return HttpResponse("Attach category has been successfully created")
    else:
        raise Http404("Request must be post")


def category(request):
    return render(request, 'example3.html')


def create_category(request):
    if request.method == 'POST':
        suffix_ = get_object_or_404(Suffix, pk=request.POST['suffix-id'])
        attach_category_ = get_object_or_404(AttachCategory, pk=request.POST['category-id'])
        category_ = Category.objects.create(title=request.POST['title'])
        category_.allowed_suffixes.add(suffix_)
        category_.allowed_attach_categories.add(attach_category_)
        return HttpResponse("Category has been successfully created")
    else:
        raise Http404("Request must be post")


def login(request):
    print('77777777778')
    print(request)
    if request.method == 'POST':
        print('h')
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            print('nnn')
            return redirect("/")
        else:
            print('----')
            messages.info(request, 'invalid username or password')
            return redirect("login")
    else:
        return render(request, 'Sign-in.html')


def sign_up(request):
    print("hello")
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'username taken')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name=name.split()[0], last_name=name.split()[-1], username=username,
                                            password=password, email=email)
            account = Account.objects.create(user=user, storage=0)
            account.save()
            print("Salamamsadkjasdjasdjaksjd")
            return redirect('login')
    else:
        return render(request, 'Sign-up.html')


def my_page(request, type, category):
    # file = File()
    # file.save()
    # content = Content (title = "hello", is_private = False, file = file)
    # content.save()
    # print(len(Content.objects.all()), 'hihihih')
    if type == 'files':
        if category == 'all':
            items = Content.objects.all()
        else:
            items = Content.objects.filter(category=category)
    elif type == 'libraries':
        if category == 'all':
            items = Library.objects.all()
        else:
            items = Library.objects.filter(category=category)
    elif type == 'shared':
        pass
    return render(request, 'my-page4.html', {'Contents': items, 'categories': Category.objects.all()})


def logout(request):
    auth.logout(request)
    return redirect("/")


def main(request):
    return render(request, 'main.html')


def test(request):
    return render(request, 'category.html')


def show_all_attribute():
    pass


def add_attribute():
    pass


def remove_attribute():
    pass


def show_all_library():
    pass


def add_library():
    pass


def remove_library():
    pass
