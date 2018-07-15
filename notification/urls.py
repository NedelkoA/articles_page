from django.conf.urls import url, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', views.CategoryListView)
router.register(r'post', views.PostListView)
router.register(r'users', views.UserListView)

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'index/', views.ArticleListView.as_view(), name='index')
]
