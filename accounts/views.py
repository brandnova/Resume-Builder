from venv import logger
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.models import UserProfile
from resumes.models import Resume
from .forms import CustomUserCreationForm, UserProfileUpdateForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.core.cache import cache
from django.utils import timezone

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            
            return redirect('dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
        # Add classes to form fields
        form.fields['username'].widget.attrs.update({
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
        })
        form.fields['password'].widget.attrs.update({
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500'
        })
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        cache_key = f'password_reset_{email}'
        last_reset = cache.get(cache_key)

        if last_reset and (timezone.now() - last_reset).total_seconds() < 300:  # 5 minutes cooldown
            messages.error(self.request, "Please wait 5 minutes before requesting another password reset.")
            return self.form_invalid(form)

        cache.set(cache_key, timezone.now(), 300)  # Set cooldown
        return super().form_valid(form)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

@login_required
def dashboard(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    completed_resumes_count = resumes.filter(is_complete=True).count()

    user = request.user  
    profile = UserProfile.objects.get(user=user) 
    # Get the domain name of the current site
    domain = request.get_host() 

    return render(request, 'accounts/dashboard.html', {
        'resumes': resumes,
        'completed_resumes_count': completed_resumes_count,
        'domain': domain, 
        'profile': profile, 
    })


@login_required
def view_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request,'accounts/view_resumes.html', {'resumes': resumes})

@login_required
def view_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'accounts/view_resumes.html', {'resumes': resumes})


@login_required
def update_profile(request):
    """
    View to handle user profile updates
    """
    if request.method == 'POST':
        form = UserProfileUpdateForm(
            request.POST, 
            request.FILES,  # Important for handling file uploads
            instance=request.user
        )
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, "Your profile has been updated successfully.")
                return redirect('dashboard')
            except ValidationError as e:
                messages.error(request, f"Validation Error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                # Consider logging the full error
                logger.error(f"Profile update error: {e}", exc_info=True)
    else:
        form = UserProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/update_profile.html', {
        'form': form,
        'user_profile': request.user.userprofile
    })