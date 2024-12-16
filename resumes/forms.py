from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Resume, PersonalInfo, WorkExperience, Education, 
    Skill, Project, Certification, Language, Reference, CustomSection
)

class ResumeForm(forms.ModelForm):
    """Base form for creating and updating Resume"""
    class Meta:
        model = Resume
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter Resume Title'
            })
        }

class PersonalInfoForm(forms.ModelForm):
    """Form for Personal Information section"""
    class Meta:
        model = PersonalInfo
        fields = [
            'full_name', 'email', 'phone', 'location', 
            'linkedin_url', 'github_url', 'website_url', 'summary', 'image'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Phone Number'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'City, Country'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'LinkedIn Profile URL (Optional)'
            }),
            'github_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'GitHub Profile URL (Optional)'
            }),
            'website_url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Personal Website URL (Optional)'
            }),
            'summary': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Professional Summary',
                'rows': 4
            }),
        }

class WorkExperienceForm(forms.ModelForm):
    """Form for Work Experience section"""
    current_job = forms.BooleanField(
        required=False,
        label='I currently work here',
        widget=forms.CheckboxInput(attrs={
            'class': 'mr-2 form-checkbox text-blue-500'
        })
    )

    class Meta:
        model = WorkExperience
        fields = ['job_title', 'company', 'location', 'start_date', 'end_date', 'description']
        widgets = {
            'job_title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Job Title'
            }),
            'company': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Company Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Location'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Job Responsibilities and Achievements',
                'rows': 4
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        current_job = cleaned_data.get('current_job')

        # If it's not a current job, end date is required
        if not current_job and not end_date:
            raise ValidationError("End date is required unless it's a current job.")

        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be later than end date.")

        # If it's a current job, set end_date to None
        if current_job:
            cleaned_data['end_date'] = None

        return cleaned_data

class EducationForm(forms.ModelForm):
    """Form for Education section"""
    currently_studying = forms.BooleanField(
        required=False,
        label='I currently study here',
        widget=forms.CheckboxInput(attrs={
            'class': 'mr-2 form-checkbox text-blue-500'
        })
    )

    class Meta:
        model = Education
        fields = ['degree', 'institution', 'location', 'start_date', 'end_date', 'major']
        widgets = {
            'degree': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Degree (e.g., Bachelor of Science)'
            }),
            'institution': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Institution Name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Location'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'major': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Major/Field of Study'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        currently_studying = cleaned_data.get('currently_studying')

        # If not currently studying, end date is required
        if not currently_studying and not end_date:
            raise ValidationError("End date is required unless you are currently studying.")

        # Validate date range
        if start_date and end_date and start_date > end_date:
            raise ValidationError("Start date cannot be later than end date.")

        # If currently studying, set end_date to None
        if currently_studying:
            cleaned_data['end_date'] = None

        return cleaned_data

class SkillForm(forms.ModelForm):
    """Form for Skills section"""
    class Meta:
        model = Skill
        fields = ['name', 'level']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Skill Name'
            }),
            'level': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }, choices=[
                ('Beginner', 'Beginner'),
                ('Intermediate', 'Intermediate'),
                ('Advanced', 'Advanced'),
                ('Expert', 'Expert')
            ])
        }

class ProjectForm(forms.ModelForm):
    """Form for Projects section"""
    class Meta:
        model = Project
        fields = ['name', 'description', 'technologies', 'start_date', 'end_date', 'url']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Project Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Project Description',
                'rows': 4
            }),
            'technologies': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Technologies Used (comma-separated)'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'url': forms.URLInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Project URL (Optional)'
            }),
        }


class CertificationForm(forms.ModelForm):
    """Form for Certifications section"""
    class Meta:
        model = Certification
        fields = ['name', 'organization', 'date_obtained', 'expiration_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Certification Name'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Issuing Organization'
            }),
            'date_obtained': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'expiration_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        date_obtained = cleaned_data.get('date_obtained')
        expiration_date = cleaned_data.get('expiration_date')

        # Validate that expiration date is after date obtained
        if date_obtained and expiration_date and date_obtained > expiration_date:
            raise ValidationError("Expiration date must be after the date obtained.")

        return cleaned_data

class LanguageForm(forms.ModelForm):
    """Form for Languages section"""
    class Meta:
        model = Language
        fields = ['name', 'proficiency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Language Name'
            }),
            'proficiency': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
            }, choices=[
                ('Beginner', 'Beginner'),
                ('Intermediate', 'Intermediate'),
                ('Advanced', 'Fluent'),
                ('Native', 'Native')
            ])
        }

class ReferenceForm(forms.ModelForm):
    """Form for References section"""
    class Meta:
        model = Reference
        fields = ['reference_name', 'position', 'organization', 'email', 'phone']
        widgets = {
            'reference_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Reference Full Name'
            }),
            'position': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Position'
            }),
            'organization': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Company/Organization'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Email Address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Phone Number'
            }),
        }

    def clean_email(self):
        """Validate email format"""
        email = self.cleaned_data.get('email')
        if email:
            # Basic email validation
            import re
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, email):
                raise forms.ValidationError("Enter a valid email address.")
        return email

class CustomSectionForm(forms.ModelForm):
    """Form for Custom Sections"""
    class Meta:
        model = CustomSection
        fields = ['section_name', 'content']
        widgets = {
            'section_name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Custom Section Name (e.g., Achievements, Volunteer Work)'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 ckeditor',
                'placeholder': 'Add detailed content for your custom section',
                'rows': 6
            })
        }

# Optional: Form for handling multiple forms simultaneously
class MultipleFormsHandler:
    """
    Helper class to handle multiple form submissions in a single view
    Usage example:
    handler = MultipleFormsHandler({
        'certification': CertificationForm,
        'language': LanguageForm,
        'reference': ReferenceForm
    })
    """
    def __init__(self, form_classes):
        """
        Initialize with a dictionary of form classes
        {
            'section_name': FormClass,
            ...
        }
        """
        self.form_classes = form_classes
        self.forms = {}

    def get_forms(self, resume, data=None, files=None):
        """
        Create form instances for each section
        
        :param resume: Resume instance
        :param data: POST data (optional)
        :param files: FILES data (optional)
        :return: Dictionary of form instances
        """
        for section, form_class in self.form_classes.items():
            # Get existing entries for the resume
            existing_entries = getattr(resume, f'{section}_set').all()
            
            if data:
                # If data is provided, instantiate form with data
                self.forms[section] = {
                    'form': form_class(data),
                    'entries': existing_entries
                }
            else:
                # If no data, just show existing entries
                self.forms[section] = {
                    'form': form_class(),
                    'entries': existing_entries
                }
        
        return self.forms

    def is_valid(self):
        """
        Validate all forms
        :return: Boolean indicating if all forms are valid
        """
        return all(
            section_data['form'].is_valid() 
            for section_data in self.forms.values()
        )

    def save(self, resume):
        """
        Save forms associated with a resume
        :param resume: Resume instance
        :return: None
        """
        for section, section_data in self.forms.items():
            form = section_data['form']
            if form.is_valid():
                # Save form with resume reference
                model_instance = form.save(commit=False)
                setattr(model_instance, 'resume', resume)
                model_instance.save()