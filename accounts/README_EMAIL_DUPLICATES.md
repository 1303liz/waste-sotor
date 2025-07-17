  b# Handling Duplicate Email Addresses

This document explains how to handle the issue of duplicate email addresses in your Django user database.

## The Problem

Django's default `User` model doesn't enforce email uniqueness at the database level, which can lead to multiple users having the same email address. This can cause issues with:

1. Password reset functionality
2. Email verification
3. User identification

## Detecting Duplicate Emails

You can run the following management command to check for duplicate emails in your system:

```bash
python manage.py check_duplicate_emails
```

This will list all email addresses that are used by multiple users, along with details about those users.

## Fixing Duplicate Emails

You have two options for fixing duplicate emails:

### Option 1: Run the Automated Fix

```bash
# First, run in dry-run mode to see what changes would be made
python manage.py fix_duplicate_emails --dry-run

# Then, if the changes look good, run without the dry-run flag
python manage.py fix_duplicate_emails
```

This will:
1. Find all duplicate email addresses
2. For each set of duplicates, keep the original email for the most appropriate user (active staff > active user > oldest user)
3. Modify the email addresses of other users to make them unique

### Option 2: Manual Fix

If you prefer to handle this manually, you can:

1. Use Django Admin to find users with duplicate emails
2. Change the email addresses as needed
3. Inform affected users about the changes

## Preventing Future Duplicates

The application has been updated to prevent new duplicate email addresses during registration by:

1. Adding email uniqueness validation in the registration form
2. Implementing robust error handling for the password reset process

## If Issues Persist

If you continue to experience issues with duplicate emails, please:

1. Check the error logs at `/logs/email.log`
2. Run `python manage.py check_duplicate_emails` to identify any remaining duplicates
3. Consider implementing a custom User model with a unique email field for new projects
