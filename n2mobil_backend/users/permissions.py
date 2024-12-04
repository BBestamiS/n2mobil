from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

class APIKeyPermission(BasePermission):
    def has_permission(self, request, view):
        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != '4815b9c3-ef30-48cd-9f41-49058a178b2b':  # API Key doğrulama
            raise AuthenticationFailed("Missing or invalid x-api-key header.")
        return True