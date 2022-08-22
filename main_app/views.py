import json
from datetime import datetime
from tkinter.messagebox import NO
from urllib import response

from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from main_app.models import Library, ContentAttribute, Attachment, Content, Library, Suffix, Category, AttachCategory, \
    File, ContentAttributeKey, Account
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages

from zipfile import ZipFile

import os
from os.path import basename


# Create your views here.
def suffix(request):
    return render(request, 'example.html')


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


def redirect_not_authenticated(request):
    if not request.user.is_authenticated:
        return redirect('/')


def redirect_admin(request):
    if request.user.is_superuser:
        return redirect('/admin')


def get_login(request, error_str):
    return render(request, 'Sign-in.html', context={'error': error_str})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            return get_login(request, 'invalid username or password')
    else:
        return render(request, 'Sign-in.html', context={'error': "None"})


def save_attr(request, content_id):
    print(request.GET)


def get_sign_up(request, error_str):
    return render(request, 'Sign-up.html', context={'error': error_str})


def sign_up(request):
    print("hello")
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            return get_sign_up(request, 'username taken')
        elif User.objects.filter(email=email).exists():
            return get_sign_up(request, 'email taken')
        else:
            user = User.objects.create_user(first_name=name.split()[0], last_name=name.split()[-1],
                                                        username=username, password=password, email=email)         

            static_file = open('static/images/default.png', 'rb')
            dynamic_file = open('dynamic/user_images/' + username +'.png', 'wb')
            dynamic_file.write(static_file.read())

            account = Account.objects.create(user=user, storage=0, image = 'dynamic/user_images/' + username +'.png')

            account.save()

            return redirect('login')
    else:
        return render(request, 'Sign-up.html', context={'error': "None"})


def get_add_content(request, err_str="None"):
    all_categories = Category.objects.all()
    attach_list = []
    for category in all_categories:
        attachs = category.allowed_attach_categories.all()
        for attach in attachs:
            attach_list.append({'category_id': category.pk, 'value': attach.pk, 'title': attach.title})
    return render(request, 'add-content.html',
                  {'categories': Category.objects.all(), 'privates': ['Private', 'Public'],
                   'attach_categories': attach_list, 'error': err_str})


def share_content(request, content_id, username):
    content = Content.objects.get(pk=content_id)
    user = User.objects.get(username=username)
    account = Account.objects.get(user=user)
    content.shared_with_accounts.add(account)
    content.save()
    account.save()
    user.save()
    return redirect('../../')


@transaction.atomic
def add_content(request):
    if request.method == 'GET':
        return get_add_content(request, "None")
    if request.method == 'POST':
        title = request.POST.get('content-title', '')
        if title == '':
            return error(request, "Title is required")
        is_private = request.POST.get('is-private', None)
        if is_private.lower() != 'public' and is_private.lower() != 'private':
            return error(request, "Privacy is required")
        else:
            if is_private.lower() == 'public':
                is_private = bool(False)
            elif is_private.lower() == 'private':
                is_private = bool(True)

        categoryID = request.POST.get('category', None)
        print('h999', categoryID)
        try:
            categoryID = int(categoryID)
        except ValueError:
            return error(request, "Category is required")
        category = Category.objects.filter(pk=categoryID).first()
        if category is None:
            return error(request, "Category does not exist")

        user = User.objects.filter(pk=request.user.id).first()
        if user is None:
            return error(request, "User does not exist")
        try:
            creator_account = Account.objects.filter(user=user).first()
            if creator_account is None:
                return error(request, "Account creator does not exist")
        except ValueError:
            return error(request, "Account is required")

        file = (request.FILES.get('content-file', None))
        if file is None:
            return error(request, 'File is required')

        idx_suffix = file.name.rfind('.')
        if idx_suffix == -1:
            return error(request, "File does not have suffix")
        suffix_title = file.name[idx_suffix + 1:]
        if len(suffix_title) == 0:
            return error(request, "File does not have proper suffix")
        if Suffix.objects.filter(title=suffix_title).exists():
            file_suffix = Suffix.objects.get(title=suffix_title)
        else:
            return error(request, "Suffix does not exist")
        if file is not None:
            content_file = File(title=file.name, creation_date=datetime.now(), modification_date=datetime.now(),
                                bytes=file.read(), suffix=file_suffix)
        else:
            return error(request, "file-content is empty")

        attach_categories_str = request.POST.get('attach-categories', None)
        attach_categories_str_lst = json.loads(attach_categories_str)
        attach_categories = []
        for x in attach_categories_str_lst:
            try:
                attach_category_id = int(x)
                attach_category = AttachCategory.objects.filter(pk=attach_category_id).first()
                if attach_category is None:
                    return error(request, "Attach category does not exist")
                attach_categories.append(attach_category)
            except ValueError:
                return error(request, "At least on of attach categories do not exist")

        attach_titles = request.POST.get('attach-titles', None)
        attach_titles = json.loads(attach_titles)

        check_arr = []
        for attach_title in attach_titles:
            if attach_title not in check_arr:
                check_arr.append(attach_title)
            else:
                return error(request, "Attach titles must be different")
        content_attachments = []
        attachments = request.FILES.getlist('attachments')
        if attachments is not None:
            if len(attachments) != len(attach_categories):
                return error(request, "Attachments and attach_categories do not have same length")

            if len(attachments) != len(attach_titles):
                return error(request, "Attachments and attach_titles do not have same length")

            for i in range(len(attachments)):
                attachment = attachments[i]
                idx_suffix = attachment.name.rfind('.')
                if idx_suffix == -1:
                    return error(request, "Attachment " + str(i) + " does not have suffix")
                suffix_title = attachment.name[idx_suffix + 1:]
                if len(suffix_title) == 0:
                    return error(request, "Attachment " + str(i) + " does not have proper suffix")
                if Suffix.objects.filter(title=suffix_title).exists():
                    attach_suffix = Suffix.objects.get(title=suffix_title)
                else:
                    return error(request, "Suffix does not exist")
                if attachment is not None:
                    attachment_file = File(title=attachment.name, creation_date=datetime.now(),
                                           modification_date=datetime.now(),
                                           bytes=attachment.read(), suffix=attach_suffix)
                attach_category = attach_categories[i]
                content_attachment = Attachment(title=attach_titles[i], attach_category=attach_category,
                                                file=attachment_file)
                content_attachments.append(content_attachment)

        print(category.title)
        print(category.allowed_suffixes.all()[0].title)
        if content_file.suffix not in category.allowed_suffixes.all():
            return error(request, "Suffix is not proper for content file")
        for content_attachment in content_attachments:
            if content_attachment.attach_category not in category.allowed_attach_categories.all():
                return error(request, "Category, Attachment, not match")
            if content_attachment.file.suffix not in content_attachment.attach_category.allowed_suffixes.all():
                return error(request, "Suffix is not proper for attachment")

        content_file.save()
        content = Content(title=title, is_private=is_private, category=category, file=content_file,
                          creator_account=creator_account)
        content.save()

        for content_attachment in content_attachments:
            content_attachment.content = content
            content_attachment.file.save()
            content_attachment.save()
    else:
        return error(request, "request is not defined")
    return render(request, 'main.html')


def error(request, str):
    return get_add_content(request, str)


def handle_uploaded_file(f):
    with open('test-file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def my_page(request, type, categoryTitle):
    auth_result = redirect_not_authenticated(request)
    if auth_result is not None:
        return auth_result

    admin_result = redirect_admin(request)
    if admin_result is not None:
        return admin_result

    account = request.user.account

    if type == 'files':
        if categoryTitle == 'all':
            privates = list(Content.objects.filter(creator_account = account))
            publics = list(Content.objects.filter(is_private = False))

            items = publics + privates
        else:
            category = Category.objects.get(title = categoryTitle)
            privates = list(Content.objects.filter(creator_account = account, category = category))
            publics = list(Content.objects.filter(is_private = False, category = category))

            items = publics + privates
        file_or_lib = 'file'

    elif type == 'libraries':
        if categoryTitle == 'all':
            items = Library.objects.filter(account = account)
        else:
            category = Category.objects.get(title = categoryTitle)
            items = Library.objects.filter(category = category, account = account)
        file_or_lib = 'lib'

    elif type == 'shared':
        contents = account.shared_with_contents.all()
        if categoryTitle == 'all':
            items = contents
        else:

            category = Category.objects.get(title = categoryTitle)
            items = contents.filter(category = category)
        file_or_lib = 'file'
        
    categories = Category.objects.all()

    return render(request, 'my-page4.html', {'view':'my-page', 'file_or_lib': file_or_lib, 'items': items, 'categories': categories,'categoryTitle': categoryTitle, 'type': type})


def library_page(request, libraryId):
    library = Library.objects.get(pk = libraryId)
    contents = library.contents.all()

    return render(request, 'my-page4.html', {'view':'library', 'file_or_lib': 'file', 'items': contents})




def logout(request):
    auth.logout(request)
    return redirect("/")


def main(request):
    return render(request, 'main.html')



def get_personal_info(request, error_str):
    return render(request, 'personal-info.html', context= {'error': error_str})


def personal_info(request):
    print('hhhh')
    if request.method == 'POST':
        print('--------------------------------')
        file = (request.FILES.get('content-file', None))
        if file is None:
            return get_personal_info(request, 'File is required')

        idx_suffix = file.name.rfind('.')
        if idx_suffix == -1:
            return get_personal_info(request, "File does not have suffix")

        suffix_title = file.name[idx_suffix + 1:]
        if len(suffix_title) == 0:
            return get_personal_info(request, "File does not have proper suffix")
        if suffix_title == 'jpg' or suffix_title == 'png':
            
            account = request.user.account
            username = request.user.username

            try:

                result_file = open('dynamic/user_images/' + username +'.png', "wb")
                result_file.write(file.read())
                request.user.account.image = 'dynamic/user_images/' + username +'.png'
                request.user.account.save()

                return get_personal_info(request, "None")
            except:
                return Http404
        else:
            return get_personal_info(request, "Suffix not acceptable")
    else:
        return get_personal_info(request, "None")


def modify_content_page(content):
    new_file = ""
    file1 = open("templates/content/content.html", 'r')
    lines = file1.readlines()
    for line in lines:
        new_file += line
        if line.find("scroll") != -1:
            for attachment in Attachment.objects.all():
                if attachment.content == content:
                    new_file += f'<b style="color: purple">{attachment.title}</b><br>\n'

    file2 = open("templates/content/content2.html", 'w')
    file2.write(new_file)
    file2.close()


def content_main_page(request, content_id):
    content = Content.objects.get(pk=content_id)
    context = {}
    context['content_id'] = content_id
    context['title'] = content.title
    context['category'] = content.category.title
    context['categoryID'] = content.category.pk
    context['creator_user'] = content.creator_account.user.username
    context['creation_date'] = content.file.creation_date
    context['privacy'] = "Private"
    if not content.is_private:
        context['privacy'] = "Public"

    all_categories = Category.objects.all()
    attach_list = []
    for category in all_categories:
        attachs = category.allowed_attach_categories.all()
        for attach in attachs:
            attach_list.append({'category_id': category.pk, 'value': attach.pk, 'title': attach.title})

    context['attach_categories'] = attach_list

    attachments = list(Attachment.objects.filter(content=content))
    attachments_send = []
    for attachment in attachments:
        attachments_send.append({'file': "", 'title': attachment.title, 'category': attachment.attach_category.pk})

    context['attachments'] = attachments_send

    attribute_keys_values = list(ContentAttribute.objects.filter(content=content))
    used_attribute_keys = []
    for akv in attribute_keys_values:
        used_attribute_keys.append(akv.key.key)
    attribute_keys = list(ContentAttributeKey.objects.filter(category=content.category))
    attribute_key_values_send = []
    counter = 0
    for ak in attribute_keys:
        if ak.key in used_attribute_keys:
            attribute_key_values_send.append({"key": ak.key, "value": attribute_keys_values[counter].value})
            counter += 1
        else:
            attribute_key_values_send.append({"key": ak.key, "value": ""})

    context["attribute_key_values"] = attribute_key_values_send
    context['error'] = "None"
    context['image_address'] = content.category.image
    print(content.category.image)
    l = list(Library.objects.filter(category=content.category))
    ll = []
    for item in l:
        ll.append({'title': item.title, 'value': item.pk})
    context['libraries'] = ll
    usernames_values = []
    for user in list(User.objects.all()):
        usernames_values.append(user.username)
    context['usernames_values'] = usernames_values
    print(context)
    return render(request, 'content.html', context)


def add_content_to_library(request, content_id):
    content = Content.objects.all().get(pk=content_id)
    print(request.GET)
    for library_dict in request.GET.items():
        library_name = library_dict[1]
        print(library_name)
        library = Library.objects.all().filter(title=library_name)[0]
        if library.category == content.category:
            content.library = library
            content.save()
            return redirect('../../')
        else:
            new_file = ""
            if request.method == "GET":
                file1 = open("templates/library_error/Copy-of-Home.html", 'r')
                lines = file1.readlines()
                for line in lines:
                    new_file += line
                    if line.find("<header") != -1:
                        new_file += '<div class=\"alert\">  <span class=\"closebtn\" onclick="this.parentElement.style.display=\'none\';\">&times;</span> This is an alert box </div>\n'
                        print("ksjfa")
                    if line.find("<form") != -1:
                        print("hi")
                        for library in Library.objects.all():
                            new_file += f'<input type = \"radio\" id = \"{library.id} \" name = \"library\" value = \"{library.title}\" > <label style = \"color: white\" for =\"library{library.id}\" > {library.title} </label > <br>\n '

            file2 = open("templates/library_error/Copy-of-Home2.html", 'w')
            file2.write(new_file)
            file2.close()
            return render(request, "../templates/library_error/Copy-of-Home2.html")


def add_to_library(request, content_id, library_id):
    content = Content.objects.get(pk=content_id)
    library = Library.objects.get(pk=library_id)
    content.library = library
    content.save()
    return redirect('../../')

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


def create_download_link(request, content_id):
    file_paths = []
    content = Content.objects.all().get(pk=content_id)
    file = open(f'static/content/Downloads/content/{content.pk}_{content.title}.{content.file.suffix.title}', 'wb')
    file.write(content.file.bytes)
    file.close()

    file_paths.append(f'static/content/Downloads/content/{content.pk}_{content.title}.{content.file.suffix.title}')
    for attachment in Attachment.objects.filter(content=content):
        path = f'static/content/Downloads/attachment/{attachment.pk}_{attachment.title}.{attachment.file.suffix.title}'
        file = open(path, 'wb')
        file.write(attachment.file.bytes)
        file.close()
        file_paths.append(path)
    with ZipFile(f'static/content/Downloads/{content.title}_{content_id}.zip', 'w') as zip:
        for file in file_paths:
            zip.write(file, basename(file))
        print(zip)
    return HttpResponse(f'/static/content/Downloads/{content.title}_{content_id}.zip')


def delete_library(request):
    print('hhhhhh')
    if request.method == 'POST':
        account = Account.objects.get(user_id=request.user.id)
        category = Category.objects.get(title=request.POST['category'])
        library = Library.objects.get(title=request.POST['title'], category_id=category.id, account_id=account.id)
        library.delete()

        return redirect('/my-page/libraries/all/')


def show_library(request):
    account = Account.objects.get(user_id=request.user.id)
    libraries = {'libraries': Library.objects.get(account_id=account.id).values()}
    # todo: change templates
    return render(request, 'Library.html', context=libraries)


def add_library(request):
    if request.method == 'POST':
        account = Account.objects.get(user_id=request.user.id)
        category = Category.objects.get(title=request.POST['category'])
        Library.objects.create(title=request.POST['library_name'], category_id=category.id, account_id=account.id)
        return redirect('/my-page/libraries/all/')
    elif request.method == 'GET':
        categories = Category.objects.all().values()
        categories = {
            'categories': categories
        }
        return render(request, 'Add-library.html', context=categories)


def show_attribute_key(request):
    account = Account.objects.get(id=request.user.id)
    attribute_keys = {'attribute_keys': ContentAttributeKey.objects.get(account_id=account.user_id).values()}
    return render(request, 'attribute-key.html', context=attribute_keys)


def add_attribute_key(request):
    if request.method == 'POST':
        account = Account.objects.get(user_id=request.user.id)
        category = Category.objects.get(title=request.POST['category'])
        ContentAttributeKey.objects.create(key=request.POST['attribute_name'], category_id=category.id,
                                           account_id=account.id)
        return HttpResponse("attribute has been successfully created")
    elif request.method == 'GET':
        categories = {
            'categories': Category.objects.all().values()
        }
        return render(request, 'add-attribute-key.html', context=categories)


def delete_attribute_key(request):
    if request.method == 'POST':
        ContentAttributeKey.objects.get(key=request.POST['attribute_key']).delete()
    return redirect('/my-page/libraries/all/')


def delete_content(request):
    if request.method == 'POST':
        print('yyyy')
        content_id = request.POST['content_id']
        content = Content.objects.get(pk = content_id)
        file = content.file
        print(content.title)
        # file.delete()
        # content.delete()
        return redirect('/my-page/files/all/')

