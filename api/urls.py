# api/urls.py
# api/urls.py (updated)
from django.urls import path
from . import views

urlpatterns = [
    path('auth/google/', views.google_auth, name='google_auth'),
    path('auth/google/callback/', views.google_callback, name='google_callback'),
    path('drive/upload/', views.drive_upload, name='drive_upload'),
    path('drive/download/', views.drive_download, name='drive_download'),
]
