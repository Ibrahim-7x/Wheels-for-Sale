from django.urls import path
from .views import *
from django.conf.urls.static import static

urlpatterns = [
    path("main/", main, name="main"),
    path("uploader/", upload_file, name="upload_file"),
    path("pick_calls/", pick_calls, name="pick_calls"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)