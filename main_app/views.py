import json
from datetime import datetime

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from main_app.models import Content, Suffix, Category, AttachCategory, File, Attachment
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from main_app.models import Account

import templates


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


@transaction.atomic
def add_content(request):
    if request.method == 'GET':
        all_categories = Category.objects.all()
        attach_list = []
        for category in all_categories:
            attachs = category.allowed_attach_categories.all()
            for attach in attachs:
                attach_list.append({'category_id': category.pk, 'value': attach.pk, 'title': attach.title})
        print(attach_list)
        return render(request, 'add-content.html',
                      {'categories': Category.objects.all(), 'privates': ['Private', 'Public'],
                       'attach_categories': attach_list})
    if request.method == 'POST':
        title = request.POST.get('content-title', '')
        print(request.POST)
        if title == '':
            return error(request, "title is required")
        is_private = request.POST.get('is-private', None)
        if is_private.lower() != 'public' and is_private.lower() != 'private':
            return error(request, "is_private is required")
        else:
            if is_private.lower() == 'public':
                is_private = bool(False)
            elif is_private.lower() == 'private':
                is_private = bool(True)

        categoryID = request.POST.get('category', None)
        try:
            categoryID = int(categoryID)
        except ValueError:
            return error(request, "category is required")
        category = Category.objects.filter(pk=categoryID).first()
        if category is None:
            return error(request, "category does not exist")

        user = User.objects.filter(pk=request.user.id).first()
        if user is None:
            return error(request, "user does not exist")
        try:
            creator_account = Account.objects.filter(user=user).first()
            if creator_account is None:
                return error(request, "account creator does not exist")
        except ValueError:
            return error(request, "account is required")

        file = (request.FILES.get('content-file', None))
        if file is None:
            return error(request, 'File is None')

        idx_suffix = file.name.rfind('.')
        if idx_suffix == -1:
            return error(request, "file does not have suffix")
        suffix_title = file.name[idx_suffix + 1:]
        if len(suffix_title) == 0:
            return error(request, "file does not have proper suffix")
        if Suffix.objects.filter(title=suffix_title).exists():
            file_suffix = Suffix.objects.get(title=suffix_title)
        else:
            return error(request, "suffix does not exist")
        if file is not None:
            content_file = File(title=file.name, creation_date=datetime.now(), modification_date=datetime.now(),
                                bytes=file.read(), suffix=file_suffix)
        else:
            return error(request, "file-content is empty")

        attach_categories_str = request.POST.get('attach-categories', None)
        print(attach_categories_str)
        attach_categories_str_lst = json.loads(attach_categories_str)
        attach_categories = []
        for x in attach_categories_str_lst:
            try:
                attach_category_id = int(x)
                attach_category = AttachCategory.objects.filter(pk=attach_category_id).first()
                if attach_category is None:
                    return error(request, "attach category does not exist")
                attach_categories.append(attach_category)
            except ValueError:
                return error(request, "at least on of attach categories do not exist")

        attach_titles = request.POST.get('attach-titles', None)
        attach_titles = json.loads(attach_titles)

        content_attachments = []
        attachments = request.FILES.getlist('attachments')
        print(attachments)
        if attachments is not None:
            if len(attachments) != len(attach_categories):
                return error(request, "attachments and attach_categories do not have same length")

            if len(attachments) != len(attach_titles):
                return error(request, "attachments and attach_titles do not have same length")

            for i in range(len(attachments)):
                attachment = attachments[i]
                idx_suffix = attachment.name.rfind('.')
                if idx_suffix == -1:
                    return error(request, "attachment " + str(i) + " does not have suffix")
                suffix_title = attachment.name[idx_suffix + 1:]
                if len(suffix_title) == 0:
                    return error(request, "attachment " + str(i) + " does not have proper suffix")
                if Suffix.objects.filter(title=suffix_title).exists():
                    attach_suffix = Suffix.objects.get(title=suffix_title)
                else:
                    return error(request, "suffix does not exist")
                if attachment is not None:
                    attachment_file = File(title=attachment.name, creation_date=datetime.now(),
                                           modification_date=datetime.now(),
                                           bytes=attachment.read(), suffix=attach_suffix)
                attach_category = attach_categories[i]
                content_attachment = Attachment(title=attach_titles[i], attach_category=attach_category,
                                                file=attachment_file)
                content_attachments.append(content_attachment)

        if content_file.suffix not in category.allowed_suffixes.all():
            print("sssss")
            return error(request, "category allowed suffix")
        for content_attachment in content_attachments:
            if content_attachment.attach_category not in category.allowed_attach_categories.all():
                return error(request, "category, attachment, not match")
            if content_attachment.file.suffix not in content_attachment.attach_category.allowed_suffixes.all():
                return error(request, "attachment allowed suffix")

        content_file.save()
        content = Content(title=title, is_private=is_private, category=category, file=content_file,
                          creator_account=creator_account)
        content.save()
        """
        content.shared_with_accounts.set(shared_with_accounts)
        for content_attachment in content_attachments:
            content_attachment.content = content
            content_attachment.file.save()
            content_attachment.save()
        for content_attribute in content_attributes:
            content_attribute.content = content
            content_attribute.save()
        """
    else:
        return error(request, "request is not post")
    return HttpResponse('<h1>Content saved</h1>')


def error(request, str):
    messages.info(request, str)
    return HttpResponse(str, status=500)


def handle_uploaded_file(f):
    with open('test-file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def my_page(request):
    # file = File()
    # file.save()
    # content = Content (title = "hello", is_private = False, file = file)
    # content.save()
    # print(len(Content.objects.all()), 'hihihih')
    return render(request, 'my-page4.html', {'contents': Content.objects.all(), 'categories': Category.objects.all()})


def logout(request):
    auth.logout(request)
    return redirect("/")


def main(request):
    return render(request, 'main.html')


def test(request):
    return render(request, 'category.html')
