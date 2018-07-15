from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Category(models.Model):
    name = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        models.CASCADE,
        null=True,
    )


class Post(models.Model):
    STATUS_DRAFT = 0
    STATUS_PUBLISHED = 100
    STATUS_REJECTED = 20
    STATUS_TRASHED = 25
    STATUS_AUTHORIZED = 80
    STATUSES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_REJECTED, 'Rejected'),
        (STATUS_TRASHED, 'Trashed'),
        (STATUS_AUTHORIZED, 'Authorized'),
    )
    status = models.SmallIntegerField(choices=STATUSES, default=STATUS_DRAFT)
    category = models.ForeignKey(
        Category,
        models.CASCADE
    )
    user = models.ForeignKey(
        User,
        models.CASCADE
    )
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Post)
def new_post(sender, **kwargs):
    if kwargs['created']:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('homepage_users', {
            'type': 'add.post',
            'message': kwargs['instance'].pk,
        })

