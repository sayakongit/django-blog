from django.urls import path
from .views import *

urlpatterns = [
    path("blogs", AdminView.as_view()),
    path("blogs/<pk>", AdminView.as_view()),
]
