from rest_framework import serializers
from blog.models import Blog
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class BlogsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Blog
        fields = '__all__'
