from django.utils import timezone
from django.conf import settings
from datetime import timedelta

class OnlineUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.is_online = True
            request.user.last_seen = timezone.now()
            request.user.save(update_fields=['is_online', 'last_seen'])

        response = self.get_response(request)
        return response
