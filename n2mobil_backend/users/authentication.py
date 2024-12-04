from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Sadece belirli endpointler için doğrulama yap
        if not request.path.startswith('/api/'):
            return None  # /api/ dışında doğrulama yapma

        api_key = request.headers.get('x-api-key')
        if not api_key or api_key != '4815b9c3-ef30-48cd-9f41-49058a178b2b':
            raise AuthenticationFailed("Missing or invalid x-api-key header.")

        return (None, None)  # Authentication success