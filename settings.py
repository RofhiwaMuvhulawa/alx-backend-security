# Add to your settings.py

# Rate limiting settings
RATELIMIT_USE_CACHE = 'default'
RATELIMIT_VIEW = 'ip_tracking.views.ratelimit_view'
RATELIMIT_FAIL_OPEN = False

# Different rate limits for authenticated vs anonymous users
RATELIMIT_RATE = {
    'anon': '5/m',  # 5 requests per minute for anonymous users
    'user': '10/m',  # 10 requests per minute for authenticated users
}

# Add the middleware
MIDDLEWARE = [
    # ... other middleware
    'ip_tracking.middleware.IPTrackingMiddleware',
    # ... other middleware
]