from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('current-date/', views.current_date, name='current_date'),
    path('get-info/', views.get_info, name='get_info'),
    path('get-chart/', views.get_chart, name='get_chart'),
    path('get-summary/', views.get_summary, name='get_summary'),
    path('download-file/', views.download_file, name='download_file'),
    path('validate-query/', views.validate_query, name='validate_query')
]
