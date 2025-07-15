# Email System Documentation

## Overview

This document provides comprehensive information about the email system used in the Waste Sorter application. The system handles user registration verification, password resets, and potentially other email notifications.

## Email Configuration

The email configuration is defined in `waste_sorter/settings.py` and uses Gmail's SMTP server:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Waste Sorter <your-email@gmail.com>'
EMAIL_TIMEOUT = 30
EMAIL_SUBJECT_PREFIX = '[Waste Sorter] '
```

### Email Security

To keep your email credentials secure:

1. Never commit your email password to version control
2. Consider using environment variables for sensitive information
3. Make sure your Gmail account has 2-factor authentication enabled and you're using an App Password

## Email Templates

### Verification Email

The email verification template is located at `templates/registration/acc_active_email.html`. It contains:

- A welcome message
- An activation button/link
- Information about the link expiration
- Contact information

### Password Reset Email

The password reset template is located at `templates/registration/password_reset_email.html`. It contains:

- A password reset button/link
- Information about the link expiration
- Security instructions

## Email Flows

### Registration Flow

1. User submits registration form
2. System creates inactive user account
3. System generates activation token
4. System sends verification email
5. User clicks verification link
6. System activates user account
7. User is redirected to login

### Password Reset Flow

1. User submits password reset form
2. System generates reset token
3. System sends password reset email
4. User clicks reset link
5. User sets new password
6. User is redirected to login

## Logging

Email activity is logged to help with debugging and monitoring:

- Log file location: `logs/email.log`
- Log format: `{levelname} {asctime} {module} {message}`
- Log levels: INFO, WARNING, ERROR

## Handling Duplicate Emails

The application includes tools to detect and fix duplicate email addresses in the user database:

1. `python manage.py check_duplicate_emails`: Lists duplicate emails
2. `python manage.py fix_duplicate_emails`: Fixes duplicate emails

For more details, see `accounts/README_EMAIL_DUPLICATES.md`.

## Testing the Email System

To test the email system:

1. Ensure your SMTP settings are correct
2. Try registering a new user
3. Check that the verification email is sent
4. Verify that the activation link works
5. Try resetting a password
6. Check that the password reset email is sent
7. Verify that the password reset link works

## Troubleshooting

If emails are not being sent:

1. Check the `logs/email.log` file for error messages
2. Verify your SMTP settings in `settings.py`
3. Make sure your Gmail account allows less secure apps or you're using an App Password
4. Check your firewall settings to ensure it allows outgoing SMTP traffic
5. Try changing `EMAIL_BACKEND` to `'django.core.mail.backends.console.EmailBackend'` temporarily to see if emails are being generated correctly
