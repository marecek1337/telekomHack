from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('current-date/', views.current_date, name='current_date'),
    path('submit-info/', views.submit_info, name='submit_info'),
    path('create-todo/', views.create_todo, name='create_todo'),
    path('download-file/', views.download_file, name='download_file')
]
