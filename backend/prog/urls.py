from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('current-date/', views.current_date, name='current_date'),
    path('get-summary/', views.get_summary, name='get_summary'),
    path('download-file/', views.download_file, name='download_file'),
    path('register/', views.register_user, name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]

