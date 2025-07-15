from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout

class SessionTimeoutMiddleware:
    """
    Custom middleware to handle session timeout warnings and auto-logout.
    This middleware will:
    1. Track when users were last active
    2. Show a warning when their session is about to expire
    3. Automatically log them out when their session expires
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Only process for authenticated users
        if request.user.is_authenticated:
            # Get the current time
            now = timezone.now()
            
            # Get the last activity time from the session
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                # Convert string time back to datetime object
                last_activity = timezone.datetime.fromisoformat(last_activity)
                
                # Calculate how long the user has been inactive
                inactive_time = now - last_activity
                
                # Calculate the warning threshold (80% of the session cookie age)
                warning_threshold = timedelta(seconds=settings.SESSION_COOKIE_AGE * 0.8)
                
                # Show a warning if the user is approaching session timeout
                if inactive_time > warning_threshold and not request.session.get('timeout_warning_shown'):
                    minutes_left = (timedelta(seconds=settings.SESSION_COOKIE_AGE) - inactive_time).total_seconds() / 60
                    messages.warning(
                        request, 
                        f"Your session will expire in approximately {int(minutes_left)} minutes due to inactivity. "
                        f"Please save your work."
                    )
                    request.session['timeout_warning_shown'] = True
            
            # Update the last activity time on each request
            request.session['last_activity'] = now.isoformat()
            # Reset the warning flag if it's been more than 5 minutes since the last warning
            if last_activity and (now - last_activity).total_seconds() < 300:
                request.session['timeout_warning_shown'] = False
                
        response = self.get_response(request)
        return response
