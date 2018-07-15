from rest_framework import serializers
from .models import Post, Category
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
        )


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
    user_repr = UserSerializer(
        read_only=True,
        source='user'
    )

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'description',
            'is_active',
            'user',
            'user_repr',
        )


class PostsSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
        write_only=True
    )
    user_repr = UserSerializer(
        read_only=True,
        source='user'
    )
    category_repr = CategorySerializer(
        read_only=True,
        source='category'
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True
    )

    class Meta:
        model = Post
        fields = (
            'id',
            'category',
            'title',
            'status',
            'content',
            'user',
            'category_repr',
            'user_repr',
        )
