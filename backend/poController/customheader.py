from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User
import os
from dotenv import load_dotenv

load_dotenv()

class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        custom_auth_header = request.headers.get('X-Custom-Auth')

        if not custom_auth_header:
            return None
        # custom authentication logic here if needed
        if custom_auth_header == os.getenv('custom_auth_header'):
            # Return a user object or None
            return (User, None)
        else:
            raise AuthenticationFailed('Invalid custom authentication header')
