"""
Management command to fix duplicate email addresses in User model.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db.models import Count
import logging

logger = logging.getLogger('django')

class Command(BaseCommand):
    help = 'Fix duplicate email addresses by appending unique identifiers'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
        
    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write('DRY RUN - No changes will be made')
            
        self.stdout.write('Finding duplicate email addresses...')
        
        # Find email addresses that appear more than once
        duplicate_emails = User.objects.values('email')\
                                      .annotate(count=Count('email'))\
                                      .filter(count__gt=1)\
                                      .values_list('email', flat=True)
        
        if not duplicate_emails:
            self.stdout.write(self.style.SUCCESS('No duplicate email addresses found!'))
            return
        
        self.stdout.write(self.style.WARNING(f'Found {len(duplicate_emails)} email addresses with duplicates'))
        
        # Track changes
        changes_count = 0
        
        # For each duplicate email, update all but the primary user
        for email in duplicate_emails:
            self.stdout.write(f'\nProcessing email: {email}')
            
            # Get all users with this email, ordered by date joined (oldest first)
            users = User.objects.filter(email=email).order_by('date_joined')
            
            # Keep the original email for:
            # 1. The first active+staff user, or
            # 2. The first active user, or
            # 3. The first user
            primary_user = None
            
            # Try to find active staff user
            active_staff_users = users.filter(is_active=True, is_staff=True)
            if active_staff_users.exists():
                primary_user = active_staff_users.first()
                self.stdout.write(f'  - Primary user (active+staff): {primary_user.username}')
            else:
                # Try to find active user
                active_users = users.filter(is_active=True)
                if active_users.exists():
                    primary_user = active_users.first()
                    self.stdout.write(f'  - Primary user (active): {primary_user.username}')
                else:
                    # Use the first/oldest user
                    primary_user = users.first()
                    self.stdout.write(f'  - Primary user (oldest): {primary_user.username}')
            
            # Modify emails for non-primary users
            for i, user in enumerate(users):
                if user != primary_user:
                    new_email = f"{user.username}_{i}@{email.split('@')[1]}"
                    self.stdout.write(f'  - Updating {user.username}: {email} → {new_email}')
                    
                    if not dry_run:
                        user.email = new_email
                        user.save(update_fields=['email'])
                        changes_count += 1
            
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f'DRY RUN - Would make {changes_count} changes'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {changes_count} duplicate email addresses'))
