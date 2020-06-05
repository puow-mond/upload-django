from django.urls import path
from . import views

urlpatterns = [
    path("", views.UploadPage.as_view(), name="upload"),
    path("<download_url>", views.Download.as_view(), name="download"),
    path("delete/<delete_url>", views.Delete.as_view(), name="delete"),
]
