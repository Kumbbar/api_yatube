from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views as token_views

from . import views

router = routers.SimpleRouter()
router.register('posts', views.PostsViewSet)
router.register('groups', views.GroupsViewSet)
router.register(
    r'posts/(?P<post_pk>\d+)/comments',
    views.CommentsViewSet,
    basename='post-comments'
)

urlpatterns = [
    path('api-token-auth/', token_views.obtain_auth_token),
    path('', include(router.urls))
]
