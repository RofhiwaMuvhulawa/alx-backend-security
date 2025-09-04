from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """Celery task to detect suspicious IPs based on request patterns"""
    # Get time range for the last hour
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # Find IPs with more than 100 requests in the last hour
    high_volume_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago
    ).values('ip_address').annotate(
        request_count=Count('id')
    ).filter(request_count__gt=100)
    
    # Find IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login', '/password/reset']
    sensitive_path_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address').annotate(
        request_count=Count('id')
    ).filter(request_count__gt=10)  # More than 10 attempts on sensitive paths
    
    # Process high volume IPs
    for ip_data in high_volume_ips:
        SuspiciousIP.objects.create(
            ip_address=ip_data['ip_address'],
            reason=f"High request volume: {ip_data['request_count']} requests in the last hour"
        )
    
    # Process sensitive path IPs
    for ip_data in sensitive_path_ips:
        SuspiciousIP.objects.create(
            ip_address=ip_data['ip_address'],
            reason=f"Suspicious access to sensitive paths: {ip_data['request_count']} attempts"
        )
    
    return f"Processed {len(high_volume_ips) + len(sensitive_path_ips)} suspicious IPs"