"""
Email utility functions with enhanced error handling and logging.
"""
import logging
import socket
import time
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from smtplib import SMTPException

# Get the custom email logger
email_logger = logging.getLogger('accounts.email')

def send_verification_email(subject, message, to_email):
    """
    Send a verification email with proper error handling and logging.
    
    Args:
        subject (str): Email subject
        message (str): Email body (HTML content)
        to_email (str): Recipient email address
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    start_time = time.time()
    
    # Apply subject prefix if configured
    if hasattr(settings, 'EMAIL_SUBJECT_PREFIX'):
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    try:
        # Get a connection with settings from settings.py
        connection = get_connection()
        
        # Log connection attempt
        email_logger.info(f"Attempting to send verification email to {to_email}")
        
        # Create email message - using EmailMultiAlternatives for better support
        email = EmailMultiAlternatives(
            subject=subject,
            body="Please enable HTML to view this email",  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
            connection=connection,
        )
        
        # Attach HTML content
        email.attach_alternative(message, "text/html")
        
        # Send the email with retry logic
        max_retries = 3
        retry_count = 0
        
        # Print a visible message to the terminal
        print("\n" + "="*80)
        print(f"🚀 SENDING VERIFICATION EMAIL to {to_email}")
        print("="*80)
        
        while retry_count < max_retries:
            try:
                sent = email.send(fail_silently=False)
                
                if sent:
                    duration = time.time() - start_time
                    success_msg = f"✅ SUCCESS: Verification email sent to {to_email} in {duration:.2f} seconds"
                    
                    # Log to file
                    email_logger.info(f"Successfully sent verification email to {to_email} in {duration:.2f} seconds")
                    
                    # Print prominent success message in terminal
                    print("\n" + "="*80)
                    print(success_msg)
                    print("="*80 + "\n")
                    
                    return True
                else:
                    retry_count += 1
                    warning_msg = f"⚠️ WARNING: Email send returned 0. Retry {retry_count}/{max_retries}"
                    
                    # Log to file
                    email_logger.warning(f"Email send returned 0. Retry {retry_count}/{max_retries}")
                    
                    # Print warning message to terminal
                    print(warning_msg)
                    
                    time.sleep(1)  # Wait a bit before retrying
            except (SMTPException, socket.error) as e:
                retry_count += 1
                error_msg = f"⚠️ ERROR: {str(e)}. Retry {retry_count}/{max_retries}"
                
                # Log to file
                email_logger.warning(f"Email send failed with error: {str(e)}. Retry {retry_count}/{max_retries}")
                
                # Print error message to terminal
                print(error_msg)
                
                time.sleep(1)  # Wait a bit before retrying
        
        # If we reach here, all retries failed
        failure_msg = f"❌ FAILED: Could not send verification email to {to_email} after {max_retries} attempts"
        
        # Log to file
        email_logger.error(f"Failed to send verification email to {to_email} after {max_retries} attempts")
        
        # Print prominent failure message in terminal
        print("\n" + "="*80)
        print(failure_msg)
        print("="*80 + "\n")
        
        return False
            
    except Exception as e:
        # Calculate duration
        duration = time.time() - start_time
        
        # Create detailed error message
        error_msg = f"❌ ERROR: Failed to send verification email to {to_email}: {str(e)}"
        
        # Log to file with full stack trace
        email_logger.error(f"Error sending verification email to {to_email} after {duration:.2f} seconds: {str(e)}", exc_info=True)
        
        # Print prominent error message in terminal
        print("\n" + "="*80)
        print(error_msg)
        print(f"Time elapsed: {duration:.2f} seconds")
        print("="*80 + "\n")
        
        return False
        
        
def send_password_reset_email(user, domain, protocol, timeout_days=3):
    """
    Send a password reset email with proper error handling and logging.
    
    Args:
        user: User object for whom to send the password reset
        domain: Current site domain
        protocol: HTTP or HTTPS
        timeout_days: Number of days the link is valid (default: 3)
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    start_time = time.time()
    
    subject = "Reset Your Password"
    # Apply subject prefix if configured
    if hasattr(settings, 'EMAIL_SUBJECT_PREFIX'):
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
    
    try:
        # Prepare token and UID for password reset
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Render the email template
        message = render_to_string('registration/password_reset_email.html', {
            'user': user,
            'domain': domain,
            'uid': uid,
            'token': token,
            'protocol': protocol,
            'timeout_days': timeout_days
        })
        
        # Log connection attempt
        email_logger.info(f"Attempting to send password reset email to {user.email}")
        
        # Get a connection with settings from settings.py
        connection = get_connection()
        
        # Create email message
        email = EmailMultiAlternatives(
            subject=subject,
            body="Please enable HTML to view this email",  # Plain text fallback
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
            connection=connection,
        )
        
        # Attach HTML content
        email.attach_alternative(message, "text/html")
        
        # Send the email with retry logic
        max_retries = 3
        retry_count = 0
        
        # Print a visible message to the terminal
        print("\n" + "="*80)
        print(f"🔑 SENDING PASSWORD RESET EMAIL to {user.email}")
        print("="*80)
        
        while retry_count < max_retries:
            try:
                sent = email.send(fail_silently=False)
                
                if sent:
                    duration = time.time() - start_time
                    success_msg = f"✅ SUCCESS: Password reset email sent to {user.email} in {duration:.2f} seconds"
                    
                    # Log to file
                    email_logger.info(f"Successfully sent password reset email to {user.email} in {duration:.2f} seconds")
                    
                    # Print prominent success message in terminal
                    print("\n" + "="*80)
                    print(success_msg)
                    print("="*80 + "\n")
                    
                    return True
                else:
                    retry_count += 1
                    warning_msg = f"⚠️ WARNING: Password reset email send returned 0. Retry {retry_count}/{max_retries}"
                    
                    # Log to file
                    email_logger.warning(f"Password reset email send returned 0. Retry {retry_count}/{max_retries}")
                    
                    # Print warning message to terminal
                    print(warning_msg)
                    
                    time.sleep(1)  # Wait a bit before retrying
            except (SMTPException, socket.error) as e:
                retry_count += 1
                error_msg = f"⚠️ ERROR: {str(e)}. Retry {retry_count}/{max_retries}"
                
                # Log to file
                email_logger.warning(f"Password reset email send failed with error: {str(e)}. Retry {retry_count}/{max_retries}")
                
                # Print error message to terminal
                print(error_msg)
                
                time.sleep(1)  # Wait a bit before retrying
        
        # If we reach here, all retries failed
        failure_msg = f"❌ FAILED: Could not send password reset email to {user.email} after {max_retries} attempts"
        
        # Log to file
        email_logger.error(f"Failed to send password reset email to {user.email} after {max_retries} attempts")
        
        # Print prominent failure message in terminal
        print("\n" + "="*80)
        print(failure_msg)
        print("="*80 + "\n")
        
        return False
            
    except Exception as e:
        # Calculate duration
        duration = time.time() - start_time
        
        # Create detailed error message
        error_msg = f"❌ ERROR: Failed to send password reset email to {user.email}: {str(e)}"
        
        # Log to file with full stack trace
        email_logger.error(f"Error sending password reset email to {user.email} after {duration:.2f} seconds: {str(e)}", exc_info=True)
        
        # Print prominent error message in terminal
        print("\n" + "="*80)
        print(error_msg)
        print(f"Time elapsed: {duration:.2f} seconds")
        print("="*80 + "\n")
        
        return False

def check_email_deliverability(email):
    """
    Check if an email address is likely to have deliverability issues.
    
    Args:
        email (str): The email address to check
        
    Returns:
        tuple: (is_deliverable, issues, suggestions)
            - is_deliverable: Boolean indicating if the email seems deliverable
            - issues: List of potential issues found
            - suggestions: List of suggestions to improve deliverability
    """
    issues = []
    suggestions = []
    
    if not email:
        issues.append("Email address is empty")
        suggestions.append("Please provide a valid email address")
        return False, issues, suggestions
    
    # Basic format validation
    if '@' not in email or '.' not in email.split('@')[1]:
        issues.append("Invalid email format")
        suggestions.append("Make sure the email includes both @ symbol and domain with a dot")
        return False, issues, suggestions
    
    # Split email into local part and domain
    local_part, domain = email.split('@')
    
    # Check local part (username)
    if len(local_part) < 1:
        issues.append("Username part is too short")
        suggestions.append("Email username must not be empty")
    
    if len(local_part) > 64:
        issues.append("Username part is too long")
        suggestions.append("Email username should be less than 64 characters")
    
    # Check for invalid characters in local part
    invalid_chars = set(['<', '>', '(', ')', '[', ']', '\\', ',', ';', ':', '"'])
    for char in invalid_chars:
        if char in local_part:
            issues.append(f"Invalid character '{char}' in email username")
            suggestions.append("Remove special characters from email username")
    
    # Check domain
    if len(domain) > 255:
        issues.append("Domain is too long")
        suggestions.append("Email domain should be less than 255 characters")
    
    # Check domain for common issues
    if domain in ['example.com', 'test.com', 'domain.com', 'email.com', 'sample.com', 'mysite.com']:
        issues.append(f"Generic domain detected: {domain}")
        suggestions.append("Use a real email address from a valid email provider")
    
    # Check for disposable email services - expanded list
    disposable_domains = [
        'mailinator.com', 'tempmail.com', 'temp-mail.org', 'guerrillamail.com', 
        'throwawaymail.com', 'yopmail.com', '10minutemail.com', 'tempmail.net',
        'dispostable.com', 'mailnesia.com', 'mailnator.com', 'trashmail.com',
        'sharklasers.com', 'guerrillamail.info', 'grr.la', 'spam4.me',
        'mailcatch.com', 'tempr.email', 'fakeinbox.com', 'getnada.com',
        'tempinbox.com', 'emailfake.com'
    ]
    if domain.lower() in disposable_domains:
        issues.append(f"Disposable email domain detected: {domain}")
        suggestions.append("Please use a permanent email address for account verification")
    
    # Check for common typos in popular domains - expanded list
    domain_typos = {
        'gmial.com': 'gmail.com',
        'gmil.com': 'gmail.com',
        'gamil.com': 'gmail.com',
        'gnail.com': 'gmail.com',
        'gmail.co': 'gmail.com',
        'gmail.con': 'gmail.com',
        'gmail.cm': 'gmail.com',
        'gmail.net': 'gmail.com',
        'gmail.org': 'gmail.com',
        'gmal.com': 'gmail.com',
        'hotmai.com': 'hotmail.com',
        'hotmial.com': 'hotmail.com',
        'hotmal.com': 'hotmail.com',
        'hotmali.com': 'hotmail.com',
        'hotmail.co': 'hotmail.com',
        'hotmail.cm': 'hotmail.com',
        'hotmail.con': 'hotmail.com',
        'hotmai.co.uk': 'hotmail.co.uk',
        'yahoocom': 'yahoo.com',
        'yaho.com': 'yahoo.com',
        'yahoo.co': 'yahoo.com',
        'yahoo.cm': 'yahoo.com',
        'yahoo.con': 'yahoo.com',
        'yahooo.com': 'yahoo.com',
        'yaoo.com': 'yahoo.com',
        'outloo.com': 'outlook.com',
        'outlok.com': 'outlook.com',
        'outlook.co': 'outlook.com',
        'outlook.con': 'outlook.com',
        'outlook.cm': 'outlook.com'
    }
    
    if domain.lower() in domain_typos:
        issues.append(f"Possible typo in domain: {domain}")
        suggestions.append(f"Did you mean {domain_typos[domain.lower()]}?")
    
    # Check for domain length
    domain_parts = domain.split('.')
    for part in domain_parts:
        if len(part) > 63:
            issues.append(f"Domain part '{part}' is too long")
            suggestions.append("Each part of the domain should be less than 64 characters")
    
    # Check if TLD seems valid (at least 2 characters)
    tld = domain_parts[-1] if domain_parts else ""
    if len(tld) < 2:
        issues.append("Invalid top-level domain (TLD)")
        suggestions.append("The email domain should end with a valid TLD like .com, .org, .edu, etc.")
    
    # Suggest specific provider help if using common email services
    if domain.lower() in ['gmail.com', 'googlemail.com']:
        suggestions.append("Gmail users: Check your Promotions tab and Spam folders. Consider adding our address to your contacts.")
    elif domain.lower() in ['outlook.com', 'hotmail.com', 'live.com', 'msn.com']:
        suggestions.append("Outlook/Hotmail users: Check your Junk Email folder and Other/Focused tabs. Add our address to your safe senders list.")
    elif domain.lower() in ['yahoo.com', 'ymail.com']:
        suggestions.append("Yahoo users: Check your Spam or Bulk Mail folders. Add our address to your contacts.")
    elif domain.lower() in ['aol.com']:
        suggestions.append("AOL users: Check your Spam folder. Add our address to your Address Book.")
    elif domain.lower() in ['icloud.com', 'me.com', 'mac.com']:
        suggestions.append("iCloud users: Check your Junk folder. Mark our emails as 'Not Junk' if found there.")
    elif domain.lower() in ['protonmail.com', 'proton.me', 'pm.me']:
        suggestions.append("ProtonMail users: Check your Spam folder. Add our address to your contacts.")
    
    # Overall deliverability assessment
    is_deliverable = len(issues) == 0
    
    # Log the check
    if is_deliverable:
        email_logger.info(f"Email {email} appears to be deliverable")
    else:
        email_logger.warning(f"Email {email} may have deliverability issues: {', '.join(issues)}")
    
    return is_deliverable, issues, suggestions
