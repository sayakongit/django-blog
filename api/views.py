from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from blog.models import Blog
from django.contrib.auth.models import User
from .serializers import BlogsSerializer


class AdminView(APIView):
    def get_object(self, pk):
        try:
            return Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        user = request.user
        if user.is_superuser:

            if pk is None:
                blogs = Blog.objects.all()
                serializer = BlogsSerializer(blogs, many=True)
                response = {
                    'data': serializer.data,
                    'count': len(serializer.data)
                }
            else:
                blog = Blog.objects.get(id=pk)
                serializer = BlogsSerializer(blog)
                response = {
                    'data': serializer.data
                }
            status = 200
        else:
            response = {
                'error': 'Admin authorization is required!'
            }
            status = 403
        return Response(response, status=status)

    def post(self, request):
        data = request.data
        user = request.user

        if user.is_superuser:
            title = data.get('title')
            content = data.get('content')

            new_blog = Blog.objects.create(
                title=title,
                content=content,
                author=User.objects.get(id=user.id)
            )
            new_blog.save()

            response = {
                'message': 'New blog added'
            }
            status = 200

        else:
            response = {
                'error': 'Admin authorization is required!'
            }
            status = 403
        return Response(response, status=status)

    def delete(self, request, pk, format=None):
        data = request.data
        user = request.user

        if user.is_superuser:
            blog = self.get_object(pk)
            blog.delete()
            response = {
                'message': 'Blog deleted'
            }
            status = 200
        else:
            response = {
                'error': 'Admin authorization is required!'
            }
            status = 403
        return Response(response, status=status)
