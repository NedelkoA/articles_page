from .models import Category, Post
from . import serializers
from django.contrib.auth.models import User
from django.views.generic import ListView
from rest_framework import viewsets, permissions
from . import permissions as custom_perms


class CategoryListView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (
        custom_perms.IsStaffOrReadOnly,
    )


class PostListView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custom_perms.IsOwnerOrReadOnly,
    )


class UserListView(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False)
    serializer_class = serializers.UserSerializer
    permission_classes = (
        custom_perms.IsAdminOrReadOnly,
    )

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateUserSerializer
        return self.serializer_class


class ArticleListView(ListView):
    model = Post
    template_name = 'notification/index.html'
    queryset = Post.objects.all().order_by('-pk')
