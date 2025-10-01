from django.shortcuts import render, redirect, get_object_or_404
from main.forms import NewsForm
from main.models import News
import datetime
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        news_list = News.objects.all()
    else:
        news_list = News.objects.filter(user=request.user)

    context = {
        'npm' : '2406428825',
        'name': 'Angelo Johenry Apituley',
        'class': 'PBP B',
        'news_list': news_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

def create_news(request):
    form = NewsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        news_entry = form.save(commit = False)
        news_entry.user = request.user
        news_entry.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }
    return render(request, "create_news.html", context)

@login_required(login_url='/login')
def show_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.increment_views()

    context = {
        'news': news
    }

    return render(request, "news_detail.html", context)

def show_xml(request):
     news_list = News.objects.all()
     xml_data = serializers.serialize("xml", news_list)
     return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    news_list = News.objects.all()
    data = [
        {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
        }
        for news in news_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, news_id):
   try:
       news_item = News.objects.filter(pk=news_id)
       xml_data = serializers.serialize("xml", news_item)
       return HttpResponse(xml_data, content_type="application/xml")
   except News.DoesNotExist:
       return HttpResponse(status=404)
   
def show_json_by_id(request, news_id):
    try:
        news = News.objects.select_related('user').get(pk=news_id)
        data = {
            'id': str(news.id),
            'title': news.title,
            'content': news.content,
            'category': news.category,
            'thumbnail': news.thumbnail,
            'news_views': news.news_views,
            'created_at': news.created_at.isoformat() if news.created_at else None,
            'is_featured': news.is_featured,
            'user_id': news.user_id,
            'user_username': news.user.username if news.user_id else None,
        }
        return JsonResponse(data)
    except News.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_news(request, id):
    news = get_object_or_404(News, pk=id)
    form = NewsForm(request.POST or None, instance=news)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_news.html", context)

def delete_news(request, id):
    news = get_object_or_404(News, pk=id)
    news.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def add_news_entry_ajax(request):
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    content = strip_tags(request.POST.get("content")) # strip HTML tags!
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_news = News(
        title=title, 
        content=content,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_news.save()

    return HttpResponse(b"CREATED", status=201)