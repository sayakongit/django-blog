from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="home"),
    path("login/", login_page, name="login"),
    path("signup/", signup_page, name="signup"),
    path("logout/", logout_view, name="logout"),
    path("blogs/", blogs_home, name="blog_home"),
    path("write_blog/", blogs_form, name="blog_form"),
    path("delete_blog/<pk>", delete_blog, name="blog_delete"),
    path('forgot_password/', forgot_password, name="forget_password"),
    path('change_password/<token>/', change_password, name="change_password"),
]
