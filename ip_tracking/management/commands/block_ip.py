from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
import ipaddress

class Command(BaseCommand):
    help = 'Block an IP address'
    
    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='IP address to block')
        parser.add_argument('--reason', type=str, help='Reason for blocking this IP')
    
    def handle(self, *args, **options):
        ip_address = options['ip_address']
        reason = options.get('reason', '')
        
        # Validate IP address
        try:
            ipaddress.ip_address(ip_address)
        except ValueError:
            raise CommandError(f"Invalid IP address: {ip_address}")
        
        # Create or update blocked IP
        blocked_ip, created = BlockedIP.objects.update_or_create(
            ip_address=ip_address,
            defaults={'reason': reason}
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS(f"Successfully blocked IP: {ip_address}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Updated blocked IP: {ip_address}"))