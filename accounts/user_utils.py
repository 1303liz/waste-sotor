from django.contrib.auth.models import User
import logging

email_logger = logging.getLogger('accounts.email')

def find_primary_user_for_email(email):
    """
    Find the most appropriate user account for a given email address.
    
    In case of multiple user accounts with the same email, we'll prioritize:
    1. Active accounts over inactive ones
    2. Staff/superuser accounts over regular ones
    3. The most recently created account
    
    Args:
        email (str): The email address to look up
        
    Returns:
        User: The most appropriate user for this email, or None if no user found
    """
    users = User.objects.filter(email=email)
    
    if not users.exists():
        return None
    
    if users.count() == 1:
        return users.first()
    
    # Log that we found duplicate emails
    email_logger.warning(f"Found {users.count()} users with the same email: {email}")
    
    # First, try to find active users
    active_users = users.filter(is_active=True)
    if active_users.exists():
        # Among active users, prefer staff/superusers
        staff_users = active_users.filter(is_staff=True)
        if staff_users.exists():
            # Return the most recently created staff user
            return staff_users.order_by('-date_joined').first()
        # Otherwise return the most recently created active user
        return active_users.order_by('-date_joined').first()
    
    # If no active users, return the most recently created user
    return users.order_by('-date_joined').first()

def get_unique_username(base_username):
    """
    Generate a unique username based on a given base username.
    Adds a number suffix if the username already exists.
    
    Args:
        base_username (str): The desired base username
        
    Returns:
        str: A unique username based on the input
    """
    username = base_username
    counter = 1
    
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
        
    return username
