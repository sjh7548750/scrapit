import base64
import os
import urllib.parse as urlparse
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime
from selenium import webdriver
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from bs4 import BeautifulSoup
from urllib.request import urlopen
from .models import Scrap, Folder
import requests
from django.core.files import File
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth


def about(request):
    return render(request, 'scrap/about.html')

def home(request, folder_id):
    ##scraps = Scrap.objects
    folder_detail = get_object_or_404(Folder,pk=folder_id)
    scraps = Scrap.objects.all().order_by('-id')
    return render(request, 'scrap/home.html', {'folder_detail':folder_detail})

def create(request, folder_id):
    scrap = Scrap() #스크랩이라는 붕어빵 틀 만듬
    scrap.address = request.POST['url'] #스크랩 주소넣기
    scrap.pub_date = timezone.datetime.now() #스크랩날짜넣기

    # external webpage에서 타이틀 넣기
    external_sites_html = urlopen(scrap.address).read()
 
    soup = BeautifulSoup(external_sites_html,  features="html5lib")
    title = soup.title.string
    scrap.title = title

    # webpage 스크린 샷찍고 파일 png로 저장
    options = webdriver.ChromeOptions()
    prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver/chromedriver.exe', chrome_options=options)
    driver.get(scrap.address)
    screenshot = driver.save_screenshot('static/save_screenshot/my_screenshot.png') #스크린샷 저장
    driver.quit()
    
    # #스크린샷을 모델 preview에 저장하기
    reopen = open("static/save_screenshot/my_screenshot.png", "rb")
    django_file = File(reopen)
    scrap.preview.save("screenshot.png", django_file, save=True) #image model에 image저장
    scrap.folder = get_object_or_404(Folder, pk=folder_id)
    #get_object_or_404(User, pk=request.GET['user_id'])
    scrap.save()
    #return render(request, 'scrap/home.html', {'folder':folder_id})
    return redirect('/folder/' + str(folder_id))

def delete(request, scrap_id):
    scraps = get_object_or_404(Scrap, pk=scrap_id)
    folder=scraps.folder.id
    scraps.delete()

    return redirect('/folder/'+str(folder))

def logout(request):
    auth.logout(request) #로그아웃 상태로 바꾸기
    return redirect('about')

def folder(request):
    folders = Folder.objects.all()
    return render(request, 'scrap/folder.html', {'folders':folders})

def foldermake(request):
    folder = Folder()
    folder.title = request.POST['folder_name']
    folder.user = request.user
    folder.save()
    return redirect('folder')

def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    folder.delete()
    return redirect('folder')

def edit(request, scrap_id):
    scrap = get_object_or_404(Scrap, pk=scrap_id)
    scrap.title = request.GET['title']
    scrap.description = request.GET['description']
    folder = scrap.folder.id
    scrap.save()
    
    return redirect('/folder/'+str(folder))

def folder_edit(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    folder.title = request.GET['title']
    folder.save()

    return redirect('folder')
