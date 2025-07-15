"""
Management command to check for and fix duplicate email addresses in User model.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
import logging

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Check for duplicate email addresses and list affected users'

    def handle(self, *args, **options):
        self.stdout.write('Checking for duplicate email addresses...')
        
        # Find email addresses that appear more than once
        duplicate_emails = User.objects.values('email')\
                                      .annotate(count=Count('email'))\
                                      .filter(count__gt=1)\
                                      .values_list('email', flat=True)
        
        if not duplicate_emails:
            self.stdout.write(self.style.SUCCESS('No duplicate email addresses found!'))
            return
        
        self.stdout.write(self.style.WARNING(f'Found {len(duplicate_emails)} duplicate email addresses:'))
        
        # For each duplicate email, show details about the users
        for email in duplicate_emails:
            users = User.objects.filter(email=email).order_by('date_joined')
            self.stdout.write(f'\nEmail: {email}')
            self.stdout.write('Users:')
            for user in users:
                self.stdout.write(f'  - ID: {user.id}, Username: {user.username}, ' +
                                 f'Active: {user.is_active}, Staff: {user.is_staff}, ' +
                                 f'Superuser: {user.is_superuser}, ' +
                                 f'Joined: {user.date_joined}')
