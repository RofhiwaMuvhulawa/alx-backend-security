from django.http import HttpResponseForbidden
from django.core.cache import cache
from ipware import get_client_ip
from django_ipgeobase import IpGeobase
from .models import RequestLog, BlockedIP

class IPTrackingMiddleware:
    """Middleware to log IP addresses and request details with geolocation"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.geo_service = IpGeobase()
        
    def __call__(self, request):
        # Get client IP address
        client_ip, is_routable = get_client_ip(request)
        
        if client_ip is not None:
            # Check if IP is blacklisted
            if BlockedIP.objects.filter(ip_address=client_ip).exists():
                return HttpResponseForbidden("Your IP address has been blocked.")
            
            # Get geolocation data with caching
            cache_key = f"geo_data_{client_ip}"
            geo_data = cache.get(cache_key)
            
            if geo_data is None:
                geo_data = self.geo_service.get_location(client_ip)
                # Cache for 24 hours
                cache.set(cache_key, geo_data, 60 * 60 * 24)
            
            # Log the request with geolocation
            RequestLog.objects.create(
                ip_address=client_ip,
                path=request.path,
                country=geo_data.get('country', ''),
                city=geo_data.get('city', '')
            )
        
        response = self.get_response(request)
        return response