from django.core.cache import cache
from django.http import HttpResponseForbidden
from django.utils import timezone
from functools import wraps
from employee.constants import RateLimitConfig


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return ip


def rate_limit(view_func):
    @wraps(view_func)
    def _wrapped(self, request, *args, **kwargs):
        # the cache key based on the user's IP
        cache_key = f'rate_limit:{get_client_ip(request)}'

        # Retrieve the current request count and timestamp from the cache
        request_count = cache.get(cache_key, 0)

        # Check if the user has exceeded the rate limit
        if request_count >= RateLimitConfig.LIMIT:
            return HttpResponseForbidden("Rate limit exceeded")

        # Update the cache with the new request count and timestamp
        cache.set(cache_key, request_count + 1, RateLimitConfig.PERIOD)

        # Call the original view function
        return view_func(self, request, *args, **kwargs)

    return _wrapped