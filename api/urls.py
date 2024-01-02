"""
API urls.
"""
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import CommentView, PostView


urlpatterns = [
    path('auth-token/', obtain_auth_token),
]

router = DefaultRouter()
router.register(r'comments', CommentView)
router.register(r'posts', PostView)

urlpatterns += router.urls
