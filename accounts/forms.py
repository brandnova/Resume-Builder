import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.EmailInput(attrs={
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Choose a username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Create a strong password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'pl-10 w-full py-3 border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update help texts to match your design
        self.fields['username'].help_text = "150 characters or fewer. Letters, digits and @/./+/-/_ only."
        self.fields['password1'].help_text = "Your password must contain at least 8 characters."
        

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = "Your password must contain at least 8 characters and can't be entirely numeric."

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-2 border rounded-md'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = "Your password must contain at least 8 characters and can't be entirely numeric."


class UserProfileUpdateForm(forms.ModelForm):
    # Personal Information Section
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your last name'
        })
    )
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Choose a username'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your email'
        })
    )
    
    # Contact Information Section
    phone_number = forms.CharField(
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter your phone number'
        })
    )
    
    # Profile Information Section
    bio = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'w-full pl-10 py-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Write a brief professional bio',
            'rows': 4
        })
    )
    
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': 'image/*',
            'x-ref': 'profilePicture'
        })
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Choose a username'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Enter your first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md',
                'placeholder': 'Enter your last name'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Exclude current user when checking for duplicate emails
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Optional: Add phone number validation
        if phone_number and not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise forms.ValidationError("Enter a valid phone number.")
        return phone_number

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        # Optional: Add bio length or content validation
        if bio and len(bio) > 500:
            raise forms.ValidationError("Bio cannot exceed 500 characters.")
        return bio

    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields['email'].initial = self.instance.email
        
        # Populate UserProfile fields if they exist
        if hasattr(self.instance, 'userprofile'):
            self.fields['phone_number'].initial = self.instance.userprofile.phone_number
            self.fields['bio'].initial = self.instance.userprofile.bio

    def save(self, commit=True):
        # Save User model fields
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        
        if commit:
            user.save()
        
        # Save UserProfile fields
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone_number = self.cleaned_data.get('phone_number')
        profile.bio = self.cleaned_data.get('bio')
        
        # Handle profile picture upload
        if self.cleaned_data.get('profile_picture'):
            profile.profile_picture = self.cleaned_data['profile_picture']
        
        profile.save()
        
        return user