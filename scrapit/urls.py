"""scrapit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib import admin
from django.urls import path, include
import scrap.views
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url, include
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', scrap.views.about, name='about'),
    path('accounts/',include('accounts.urls')),
    path('social/', include('allauth.urls')),
    path('logout/', scrap.views.logout, name="logout"),
    path('foldermake/', scrap.views.foldermake, name="foldermake"),
    path('delete_folder/<int:folder_id>', scrap.views.delete_folder, name='delete_folder'),
    path('folder/<int:folder_id>', scrap.views.home, name='home'),
    path('folder/', scrap.views.folder, name="folder"),
    path('create/<int:folder_id>', scrap.views.create, name="create"),
    path('delete/<int:scrap_id>', scrap.views.delete, name="delete"),
    path('edit/<int:scrap_id>', scrap.views.edit, name="edit"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)