
from multiprocessing.forkserver import connect_to_new_process
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from main_app.models import Content, Suffix, Category, AttachCategory, File
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from main_app.models import Account

import templates


# Create your views here.
def suffix(request):
    return render(request, 'example.html')

#def content_main_page(request, content_id):


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


def add_content(request):
    # print(request.data)
    if request.method == 'GET':
        return render(request, 'add-content.html')
    if request.method == 'POST':
        title = request.POST.get('title', '')
        if title == '':
            return error(request, "title is required")
        is_private = request.POST.get('is-private', None)
        if is_private.lower() != 'false' and is_private.lower() != 'true':
            return error(request, "is_private is required")
        else:
            if is_private.lower() == 'false':
                is_private = bool(False)
            elif is_private.lower() == 'true':
                is_private = bool(True)

        categoryID = request.POST.get('category-id', None)
        try:
            categoryID = int(categoryID)
        except ValueError:
            return error(request, "category is required")
        category = Category.objects.filter(pk=categoryID).first()
        if category is None:
            return error(request, "category does not exist")

        """
        libraryID = request.POST.get('library-id', None)
        if libraryID is not None and libraryID != '':
            try:
                libraryID = int(libraryID)
                library = Library.objects.filter(pk=libraryID).first()
                if library is None:
                    return error(request, "library does not exist")
            except ValueError:
                return error(request, "library does not exist")
        else:
            library = None
        """
        creator_accountID = request.POST.get('creator-account-id', -1)
        try:
            creator_accountID = int(creator_accountID)
            creator_account = Account.objects.filter(pk=creator_accountID).first()
            if creator_account is None:
                return error(request, "creator account does not exist")
        except ValueError:
            return error(request, "account is required")

        """
        shared_with_accountIDs_str = request.POST.get('shared-with-account-ids', None)
        shared_with_accounts = []
        if shared_with_accountIDs_str is not None and shared_with_accountIDs_str != "":
            shared_with_accountIDs_str_lst = json.loads(shared_with_accountIDs_str)
            for x in shared_with_accountIDs_str_lst:
                try:
                    shared_with_account_id = int(x)
                    shared_with_account = Account.objects.filter(pk=shared_with_account_id).first()
                    if shared_with_account is None:
                        return error(request, "share account does not exist")
                    shared_with_accounts.append(shared_with_account)
                except ValueError:
                    return error(request, "at least one of the shared accounts do not exist")

        content_attributes_str = request.POST.get('content-attributes', None)
        content_attributes_lst = json.loads(content_attributes_str)
        content_attributes = []
        for x in content_attributes_lst:
            key = x['key']
            value = x['value']
            # ca = ContentAttribute.objects.filter(key=key).first()
            # if ca is not None:
                # if ca matches category:
            content_attribute = ContentAttribute(key=key, value=value)
            content_attributes.append(content_attribute)
            #else:
            #    return error(request, "content attribute does not exist")
        """
        attach_categories_str = request.POST.get('attach-categories', None)
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

        attach_category_titles = request.POST.get('attach-category-titles', None)
        attach_category_titles = json.loads(attach_category_titles)

        file = (request.FILES.get('content-file', None))
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
        content_attachments = []
        attachments = request.FILES.getlist('attachments')
        if attachments is not None:
            if len(attachments) != len(attach_categories):
                return error(request, "attachments and attach_categories do not have same length")

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
                                           bytes=file.read(), suffix=attach_suffix)
                attach_category = attach_categories[i]
                content_attachment = Attachment(title=attach_category_titles[i], attach_category=attach_category,
                                                file=attachment_file)
                content_attachments.append(content_attachment)

        if not category.allowed_suffixes.filter(content_file.suffix).exists():
            error(request, "category allowed suffix")
        for content_attachment in content_attachments:
            if not content_attachment.attach_category.allowed_suffixes.filter(content_attachment.file.suffix).exists():
                error(request, "attachment allowed suffix")
            if not category.allowed_attach_categories.filter(content_attachment.attach_category).exists():
                error(request, "category, attachment, not match")
        return HttpResponse("str", status=500)
        content_file.save()
        content = Content(title=title, is_private=is_private, category=category, file=content_file, library=library,
                          creator_account=creator_account)

        content.save()
        content.shared_with_accounts.set(shared_with_accounts)
        for content_attachment in content_attachments:
            content_attachment.content = content
            content_attachment.file.save()
            content_attachment.save()
        for content_attribute in content_attributes:
            content_attribute.content = content
            content_attribute.save()
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
    return render(request, 'my-page4.html', {'contents': Content.objects.all(), 'categories':Category.objects.all()})


def logout(request):
    auth.logout(request)
    return redirect("/")


def main(request):
    return render(request, 'main.html')

def test(request):
    return render(request, 'category.html')
