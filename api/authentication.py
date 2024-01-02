"""
API authentication.
"""
from rest_framework.authentication import TokenAuthentication


class BearerAuthentication(TokenAuthentication):
    """Bearer authentication."""
    keyword = "Bearer"
