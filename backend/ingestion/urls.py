from django.urls import path
from .views import upload_sap

urlpatterns = [
    path('upload/sap/', upload_sap),
]