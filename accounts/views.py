from itertools import chain
from venv import logger
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.db.models import Count
from accounts.models import UserProfile
from resumes.models import DOCXDownload, PDFDownload, Resume
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
    user = request.user
    profile = UserProfile.objects.get(user=user)
    domain = request.get_host()
    
    # Resume statistics
    resumes = Resume.objects.filter(user=user).order_by('-created_at')
    completed_resumes_count = resumes.filter(is_complete=True).count()
    
    # Activity metrics
    recent_activities = []
    
    # Resume updates in last 24 hours
    last_24h_updates = resumes.filter(
        updated_at__gte=timezone.now() - timezone.timedelta(days=1)
    ).count()
    
    # Monthly growth
    last_month = timezone.now() - timezone.timedelta(days=30)
    current_month_resumes = resumes.filter(created_at__gte=last_month).count()
    previous_month_resumes = resumes.filter(
        created_at__gte=last_month - timezone.timedelta(days=30),
        created_at__lt=last_month
    ).count()
    
    monthly_growth = 0
    if previous_month_resumes > 0:
        monthly_growth = ((current_month_resumes - previous_month_resumes) / previous_month_resumes) * 100
    
    # Template usage statistics
    template_usage = list(Resume.objects.filter(user=user)
    .values('template__name')
    .annotate(count=Count('id')))

    total_resumes = sum(t['count'] for t in template_usage)
    colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6']

    for i, template in enumerate(template_usage):
        template['percentage'] = (template['count'] / total_resumes * 100)
        template['color'] = colors[i % len(colors)]
    
    # Download statistics
    pdf_downloads = PDFDownload.objects.filter(user=user).count()
    docx_downloads = DOCXDownload.objects.filter(user=user).count()
    
    # Recent activities tracking
    activities = []
    
    # Resume updates
    for resume in resumes[:5]:
        activities.append({
            'type': 'update',
            'title': resume.title,
            'timestamp': resume.updated_at,
            'icon': 'fa-pencil-alt',
            'color': 'blue'
        })
    
    # Recent downloads
    recent_downloads = list(chain(
        PDFDownload.objects.filter(user=user).order_by('-created_at')[:3],
        DOCXDownload.objects.filter(user=user).order_by('-created_at')[:3]
    ))
    for download in sorted(recent_downloads, key=lambda x: x.created_at, reverse=True)[:5]:
        activities.append({
            'type': 'download',
            'title': download.resume.title,
            'timestamp': download.created_at,
            'icon': 'fa-download',
            'color': 'green'
        })
    
    # Sort activities by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    context = {
        'resumes': resumes,
        'completed_resumes_count': completed_resumes_count,
        'domain': domain,
        'profile': profile,
        'last_24h_updates': last_24h_updates,
        'monthly_growth': monthly_growth,
        'template_usage': template_usage,
        'pdf_downloads': pdf_downloads,
        'docx_downloads': docx_downloads,
        'activities': activities[:5],
        'completion_rate': (completed_resumes_count / resumes.count() * 100) if resumes.exists() else 0,
    }
    
    return render(request, 'accounts/dashboard.html', context)



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