from django.shortcuts import redirect
from django.urls import resolve, reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of URLs that don't require authentication
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
            'tips_home',
            'tip_detail',
            'category_tips',
        ]

        # Check if current URL name matches any in the public URLs list
        current_url_name = resolve(request.path_info).url_name
        
        # If user is not authenticated and URL is not public, redirect to login
        if not request.user.is_authenticated and current_url_name not in public_urls:
            # Store the current URL in the session for post-login redirect
            request.session['next'] = request.get_full_path()
            return redirect('login')

        response = self.get_response(request)
        return response
