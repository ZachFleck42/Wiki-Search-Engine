from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', views.search),
    path('crawl/', views.crawl),
]
