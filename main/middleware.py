from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class AnonymousOnInvalidTokenMiddleware:
    """
    If JWT token is invalid, set request.user to AnonymousUser instead of raising 401.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only process API endpoints
        if request.path.startswith('/api/'):
            try:
                user_auth_tuple = JWTAuthentication().authenticate(request)
                if user_auth_tuple:
                    request.user, request.auth = user_auth_tuple
                else:
                    request.user = AnonymousUser()
            except AuthenticationFailed:
                request.user = AnonymousUser()
        response = self.get_response(request)
        return response

class InvalidTokenAsAnonymousMiddleware(AnonymousOnInvalidTokenMiddleware):
    pass
