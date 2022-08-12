from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_protect
from main_app.models import Suffix, Category, AttachCategory

import templates


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
