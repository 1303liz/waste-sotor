from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, JsonResponse
import datetime
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from django.db import IntegrityError
import logging
from .utils import send_verification_email, send_password_reset_email, check_email_deliverability
from .user_utils import find_primary_user_for_email, get_unique_username
from django.contrib.auth.decorators import login_required

# Get the custom email logger
email_logger = logging.getLogger('accounts.email')

@login_required
def profile(request):
    """User profile page showing account information and stats"""
    from waste_logs.models import WasteLog, WasteEntry
    from recycle_tips.models import Tip
    
    # Get user statistics
    user_waste_logs = WasteLog.objects.filter(user=request.user).count()
    user_waste_entries = WasteEntry.objects.filter(waste_log__user=request.user).count()
    user_tips = Tip.objects.filter(author=request.user).count() if hasattr(Tip, 'author') else 0
    
    # Get recent activity
    recent_logs = WasteLog.objects.filter(user=request.user).order_by('-created_at')[:5]
    recent_entries = WasteEntry.objects.filter(waste_log__user=request.user).order_by('-created_at')[:5]
    
    context = {
        'user_waste_logs': user_waste_logs,
        'user_waste_entries': user_waste_entries,
        'user_tips': user_tips,
        'recent_logs': recent_logs,
        'recent_entries': recent_entries,
    }
    
    return render(request, 'accounts/profile.html', context)

def register(request):
    if request.method == 'POST':
        print("\n" + "*"*80)
        print("📝 PROCESSING NEW USER REGISTRATION")
        print("*"*80)
        
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Extract email for logging
            to_email = form.cleaned_data.get('email')
            
            print(f"👤 New registration attempt: {to_email}")
            email_logger.info(f"New user registration attempt: {to_email}")
            
            # Check email deliverability before creating account
            print("🔍 Checking email deliverability...")
            is_deliverable, issues, suggestions = check_email_deliverability(to_email)
            
            # If there are issues with the email, warn the user but don't prevent registration
            if not is_deliverable:
                print(f"⚠️ Email deliverability issues detected: {', '.join(issues)}")
                for issue in issues:
                    messages.warning(request, f"Potential email issue: {issue}")
                for suggestion in suggestions:
                    messages.info(request, suggestion)
                
                # Add an extra warning about verification emails possibly not being delivered
                messages.warning(request, 
                    "Your email address may have deliverability issues. "
                    "If you don't receive a verification email, please check your spam folder "
                    "or consider registering with a different email address."
                )
            else:
                print("✅ Email appears deliverable")
            
            # Create the user account
            print("👤 Creating new user account...")
            user = form.save()
            email_logger.info(f"Created new user: username={user.username}, email={user.email}")
            print(f"✅ User created: {user.username}")
            
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            
            # Generate activation token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(f"🔑 Generated activation token for user {user.username}")
            
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': 'http' if request.is_secure() == False else 'https'
            })
            
            # Store email provider info for custom help
            email_domain = to_email.split('@')[1].lower() if '@' in to_email else ''
            request.session['email_domain'] = email_domain
            
            # Use the utility function to send email with proper error handling
            print("📧 Attempting to send verification email...")
            if send_verification_email(mail_subject, message, to_email):
                # Store email and sent time in session for reference
                from datetime import datetime
                now = datetime.now()
                timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                
                request.session['verification_email'] = to_email
                request.session['verification_sent_time'] = timestamp
                
                print(f"✅ Verification email successfully sent at {timestamp}")
                messages.success(request, f"Verification email sent to {to_email}")
                
                # Log summary of registration process
                email_logger.info(f"Registration completed successfully for {user.username} ({to_email})")
            else:
                print("❌ Failed to send verification email")
                messages.error(request, "Failed to send verification email. Please try again later or contact support.")
                email_logger.error(f"Registration incomplete for {user.username} ({to_email}) - email sending failed")
                
            print("*"*80 + "\n")
            return redirect('verification_sent')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def activate(request, uidb64, token):
    print("\n" + "*"*80)
    print("🔐 PROCESSING ACCOUNT ACTIVATION REQUEST")
    print("*"*80)
    
    print(f"🔑 Activation attempt with UID: {uidb64}")
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(f"🔍 Looking up user with ID: {uid}")
        user = User.objects.get(pk=uid)
        print(f"✅ Found user: {user.username} ({user.email})")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        print(f"❌ Account activation failed: {str(e)}")
        email_logger.error(f"Account activation failed with invalid UID: {uidb64}, Error: {str(e)}")
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        print(f"✅ Token valid for user: {user.username}")
        
        # Check if already active
        if user.is_active:
            print(f"ℹ️ Account for {user.username} was already active")
            email_logger.info(f"Activation attempt for already active account: {user.username} ({user.email})")
        else:
            print(f"✅ Activating account for {user.username}")
            user.is_active = True
            user.save()
            email_logger.info(f"Account activated successfully for user: {user.username} ({user.email})")
        
        print("🔓 Logging user in")
        login(request, user)
        
        print("*"*80 + "\n")
        return redirect('dashboard')
    else:
        if user:
            print(f"❌ Invalid token for user: {user.username}")
            email_logger.warning(f"Invalid token for account activation: user={user.username}, token={token}")
        else:
            print("❌ Invalid activation link - no matching user found")
        
        print("*"*80 + "\n")
        return render(request, 'registration/activation_invalid.html')

def verification_sent(request):
    email = request.session.get('verification_email', '')
    sent_time = request.session.get('verification_sent_time', '')
    
    # Check if the user is trying to access the verification page without having registered
    if not email:
        messages.info(request, "You need to register or provide an email for verification first.")
        return redirect('register')
    
    # Track verification attempts in session
    if not request.session.get('verification_attempts'):
        request.session['verification_attempts'] = 1
        request.session['first_verification_time'] = sent_time
    
    context = {
        'email': email,
        'sent_time': sent_time
    }
    return render(request, 'registration/verification_sent.html', context)

def resend_verification(request):
    if request.method == 'POST':
        print("\n" + "*"*80)
        print("🔄 PROCESSING VERIFICATION EMAIL RESEND REQUEST")
        print("*"*80)
        
        email = request.POST.get('email')
        print(f"📧 Resend verification requested for: {email}")
        email_logger.info(f"Resend verification requested for: {email}")
        
        # Check email deliverability
        print("🔍 Checking email deliverability...")
        is_deliverable, issues, suggestions = check_email_deliverability(email)
        
        # If there are issues with the email, warn the user
        if not is_deliverable:
            print(f"⚠️ Email deliverability issues detected: {', '.join(issues)}")
            for issue in issues:
                messages.warning(request, f"Potential email issue: {issue}")
            for suggestion in suggestions:
                messages.info(request, suggestion)
        else:
            print("✅ Email appears deliverable")
                
        try:
            # Find the user (handle potential duplicates)
            print("🔍 Looking up user account...")
            user = find_primary_user_for_email(email)
            if not user:
                print("❌ No user found with that email")
                messages.error(request, f"No registered account found with email {email}. Please register first.")
                email_logger.warning(f"Verification email requested for non-existent account: {email}")
                return redirect('register')
                
            if not user.is_active:
                print(f"✅ Found inactive user: {user.username}")
                
                # Generate new verification email
                print("🔑 Generating new activation token...")
                current_site = get_current_site(request)
                mail_subject = 'Activate your account'
                
                # Generate token for logging
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': uid,
                    'token': token,
                    'protocol': 'http' if request.is_secure() == False else 'https'
                })
                
                # Store email provider info for custom help
                email_domain = email.split('@')[1].lower() if '@' in email else ''
                request.session['email_domain'] = email_domain
                
                # Use the utility function to send email with proper error handling
                print("📧 Attempting to resend verification email...")
                if send_verification_email(mail_subject, message, user.email):
                    # Store email and sent time in session for reference
                    from datetime import datetime
                    now = datetime.now()
                    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
                    
                    request.session['verification_email'] = email
                    request.session['verification_sent_time'] = timestamp
                    
                    # Track number of verification attempts
                    attempts = request.session.get('verification_attempts', 0) + 1
                    request.session['verification_attempts'] = attempts
                    
                    print(f"🔢 Verification attempt #{attempts}")
                    
                    # If this is the first attempt, also store the time as first attempt time
                    if 'first_verification_time' not in request.session:
                        request.session['first_verification_time'] = request.session['verification_sent_time']
                        print(f"⏱️ First verification attempt recorded at {timestamp}")
                    
                    # If there have been many attempts, suggest alternative approaches
                    if attempts >= 3:
                        print(f"⚠️ Multiple verification attempts detected: {attempts}")
                        messages.warning(request, 
                            "You've requested multiple verification emails. If you're still having issues, "
                            "try using a different email provider or check your spam/junk folder."
                        )
                    
                    messages.success(request, f'Verification email resent to {email}. Please check your inbox.')
                    print(f"✅ Verification email successfully resent at {timestamp}")
                else:
                    print("❌ Failed to resend verification email")
                    messages.error(request, "Failed to resend verification email. Please try again later or contact support.")
            else:
                print(f"ℹ️ Account already active for {user.username}")
                email_logger.info(f"Resend verification attempted for already active account: {email}")
                messages.info(request, 'Your account is already active. Please login.')
        except User.DoesNotExist:
            print("❌ No user found with that email address")
            email_logger.warning(f"Resend verification attempted for non-existent email: {email}")
            messages.error(request, 'No user found with that email.')
        
        print("*"*80 + "\n")
        return redirect('verification_sent')
    return render(request, 'registration/resend_verification.html')

def check_verification_status(request):
    """
    Check the status of email verification and provide feedback.
    This is an AJAX endpoint that returns JSON with verification status info.
    """
    if request.method == 'GET':
        email = request.session.get('verification_email', '')
        if not email:
            return JsonResponse({
                'status': 'unknown',
                'message': 'No verification in progress'
            })
            
        # Check if user exists and is active
        try:
            user = find_primary_user_for_email(email)
            if user and user.is_active:
                # User has been verified
                return JsonResponse({
                    'status': 'verified',
                    'message': 'Your account has been verified! You can now log in.',
                    'redirect_url': '/login/'
                })
            elif user:
                # Get timing information
                sent_time = request.session.get('verification_sent_time', '')
                attempts = request.session.get('verification_attempts', 1)
                
                # Calculate time elapsed since first verification attempt
                now = datetime.datetime.now()
                first_time = request.session.get('first_verification_time', sent_time)
                
                if first_time:
                    try:
                        first_time_obj = datetime.datetime.strptime(first_time, '%Y-%m-%d %H:%M:%S')
                        elapsed_minutes = (now - first_time_obj).total_seconds() / 60
                    except:
                        elapsed_minutes = 0
                else:
                    elapsed_minutes = 0
                
                # Provide different advice based on elapsed time
                if elapsed_minutes > 30:
                    extra_advice = ("It's been over 30 minutes. The email might be delayed or filtered. "
                                   "Try checking all folders including Spam/Junk.")
                elif elapsed_minutes > 10:
                    extra_advice = ("It's been over 10 minutes. If you still haven't received the email, "
                                   "check your Spam/Junk folder.")
                else:
                    extra_advice = "Please allow a few minutes for the email to arrive."
                
                return JsonResponse({
                    'status': 'pending',
                    'message': f'Verification email sent to {email}. {extra_advice}',
                    'attempts': attempts,
                    'elapsed_minutes': round(elapsed_minutes)
                })
            else:
                # User doesn't exist
                return JsonResponse({
                    'status': 'error',
                    'message': 'No user found with that email.'
                })
        except Exception as e:
            email_logger.error(f"Error checking verification status: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while checking verification status.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    })

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        if not user.is_active:
            messages.error(self.request, 'Please verify your email before logging in.')
            return HttpResponseRedirect('/verification-sent/')
        return super().form_valid(form)
    
    def get_success_url(self):
        # First check if 'next' parameter was stored in session
        next_url = self.request.session.pop('next', None)
        if next_url:
            return next_url
            
        # Then check for 'next' parameter in GET or POST data
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
            
        # Default to dashboard if no redirect URL is found
        return '/dashboard/'

def custom_logout(request):
    """
    Custom logout view that logs the event and shows a confirmation page.
    Handles both POST requests (from the logout form) and GET requests (direct URL access).
    POST method is preferred for security reasons (CSRF protection).
    """
    # Only process logout for POST requests or authenticated users on GET requests
    if request.method == 'POST' or request.user.is_authenticated:
        # Track user info before logging them out
        user_info = {'was_authenticated': False}
        if request.user.is_authenticated:
            user_info = {
                'was_authenticated': True,
                'username': request.user.username,
                'email': request.user.email,
            }
            
            # Log the logout event
            email_logger.info(f"User logout initiated: {user_info['username']} ({user_info['email']})")
            print(f"\n{'*'*80}\n🔒 USER LOGOUT: {user_info['username']} ({user_info['email']})\n{'*'*80}\n")
        
        # Use Django's built-in logout function
        from django.contrib.auth import logout
        logout(request)
        
        # Add a success message if the user was authenticated
        if user_info['was_authenticated']:
            messages.success(request, f"You have been successfully logged out. See you next time!")
            email_logger.info(f"User logout completed: {user_info['username']} ({user_info['email']})")
        
        # Render the logout confirmation page
        return render(request, 'registration/logged_out.html')
    
    else:
        # For GET requests when not logged in, redirect to the homepage
        messages.info(request, "You are already logged out.")
        return redirect('/')

class CustomPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = '/accounts/password-reset/done/'
    
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        
        # Instead of sending to all users with this email, find the primary one
        user = find_primary_user_for_email(email)
        
        # Get the current site
        current_site = get_current_site(self.request)
        protocol = 'https' if self.request.is_secure() else 'http'
        
        if user:
            try:
                # Send the password reset email using our utility function
                success = send_password_reset_email(
                    user=user,
                    domain=current_site.domain,
                    protocol=protocol,
                    timeout_days=3
                )
                
                if success:
                    email_logger.info(f"Password reset email sent for primary user: {user.username} ({email})")
                else:
                    email_logger.error(f"Failed to send password reset email for primary user: {user.username} ({email})")
            except Exception as e:
                email_logger.error(f"Exception sending password reset email to {email}: {str(e)}", exc_info=True)
        else:
            # Log the attempt but don't reveal if user exists to prevent email enumeration
            email_logger.warning(f"Password reset attempted for non-existent email: {email}")
            
        # Always redirect to the success page regardless of whether the user exists
        # This prevents email enumeration attacks
        return HttpResponseRedirect(self.get_success_url())
