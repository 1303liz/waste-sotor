from django.shortcuts import redirect
from django.urls import resolve, reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require authentication (only auth-related pages)
        public_urls = [
            'login',
            'register',
            'password_reset',
            'password_reset_done',
            'password_reset_confirm',
            'password_reset_complete',
            'activate',
            'verification_sent',
            'resend_verification',
            'check_verification_status',
        ]

        # Skip middleware for admin URLs and static files
        if request.path.startswith('/admin/') or request.path.startswith('/static/') or request.path.startswith('/media/'):
            response = self.get_response(request)
            return response

        # Check if current URL name matches any in the public URLs list
        try:
            current_url_name = resolve(request.path_info).url_name
        except:
            current_url_name = None
        
        # If user is not authenticated and URL is not public, redirect to login
        if not request.user.is_authenticated and current_url_name not in public_urls:
            # Store the current URL in the session for post-login redirect
            request.session['next'] = request.get_full_path()
            return redirect('login')

        response = self.get_response(request)
        return response
