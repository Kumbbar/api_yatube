from rest_framework import viewsets, mixins
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import permissions

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS', 'POST'):
            return True
        return obj.author == request.user


class PostsViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupsViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise NotFound('Category not found')
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user, post=post)
