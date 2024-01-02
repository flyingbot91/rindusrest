"""
API serializers.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from api.authentication import BearerAuthentication
from api.models import Comment, Post
from api.serializers import CommentSerializer, PostSerializer


class CommentView(ModelViewSet):
    """API endpoint for api.models.Comment operations."""
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class PostView(ModelViewSet):
    """API endpoint for api.models.Post operations."""
    authentication_classes = (BearerAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
