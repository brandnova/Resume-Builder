from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os
import hashlib
import pdfkit
import hmac
import json
import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.template import Template, Context

from core.models import SiteSettings

from .models import (
    PDFDownload, Resume, PersonalInfo, ResumeTemplate, UserTemplate, WorkExperience, Education, 
    Skill, Project, Certification, Language, Reference, CustomSection
)
from .forms import (
    CertificationForm, CustomSectionForm, LanguageForm, ReferenceForm, ResumeForm, PersonalInfoForm, WorkExperienceForm, 
    EducationForm, SkillForm, ProjectForm
)


@login_required
def create_resume(request):
    """Initial step to create a new resume"""
    if request.method == 'POST':
        form = ResumeForm(request.POST)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = request.user
            resume.save()
            return redirect('resume_personal_info', resume_slug=resume.slug)
    else:
        form = ResumeForm()
    
    return render(request, 'resumes/create_resume.html', {
        'form': form,
        'section': 'resume_title'
    })

@login_required
def personal_info(request, resume_slug):
    """Step to add personal information to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    try:
        personal_info = resume.personalinfo
    except PersonalInfo.DoesNotExist:
        personal_info = None

    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request.FILES, instance=personal_info)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.resume = resume
            personal_info.save()
            
            # Mark resume as in progress
            resume.is_complete = False
            resume.save()
            
            return redirect('resume_work_experience', resume_slug=resume.slug)
    else:
        form = PersonalInfoForm(instance=personal_info)
    
    return render(request, 'resumes/personal_info.html', {
        'form': form,
        'resume': resume,
        'section': 'personal_info'
    })

@login_required
def work_experience(request, resume_slug):
    """Step to add work experiences to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    work_experiences = resume.workexperience_set.all()

    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_exp = form.save(commit=False)
            work_exp.resume = resume
            work_exp.save()
            messages.success(request, 'Work experience added successfully.')
            return redirect('resume_work_experience', resume_slug=resume.slug)
    else:
        form = WorkExperienceForm()

    return render(request, 'resumes/work_experience.html', {
        'form': form,
        'work_experiences': work_experiences,
        'resume': resume,
        'section': 'work_experience'
    })

@login_required
def delete_work_experience(request, resume_slug, work_exp_id):
    """Delete a specific work experience entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    work_exp = get_object_or_404(WorkExperience, id=work_exp_id, resume=resume)
    
    if request.method == 'POST':
        work_exp.delete()
        messages.success(request, 'Work experience removed successfully.')
        return redirect('resume_work_experience', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': work_exp,
        'resume': resume
    })

@login_required
def education(request, resume_slug):
    """Step to add education entries to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    education_entries = resume.education_set.all()

    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education_entry = form.save(commit=False)
            education_entry.resume = resume
            education_entry.save()
            messages.success(request, 'Education entry added successfully.')
            return redirect('resume_education', resume_slug=resume.slug)
    else:
        form = EducationForm()

    return render(request, 'resumes/education.html', {
        'form': form,
        'education_entries': education_entries,
        'resume': resume,
        'section': 'education'
    })

@login_required
def delete_education(request, resume_slug, education_id):
    """Delete a specific education entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    education_entry = get_object_or_404(Education, id=education_id, resume=resume)
    
    if request.method == 'POST':
        education_entry.delete()
        messages.success(request, 'Education entry removed successfully.')
        return redirect('resume_education', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': education_entry,
        'resume': resume
    })

@login_required
def skills(request, resume_slug):
    """Step to add skills to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    skills = resume.skill_set.all()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.resume = resume
            skill.save()
            messages.success(request, 'Skill added successfully.')
            return redirect('resume_skills', resume_slug=resume.slug)
    else:
        form = SkillForm()

    return render(request, 'resumes/skills.html', {
        'form': form,
        'skills': skills,
        'resume': resume,
        'section': 'skills'
    })

@login_required
def delete_skill(request, resume_slug, skill_id):
    """Delete a specific skill entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    skill = get_object_or_404(Skill, id=skill_id, resume=resume)
    
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill removed successfully.')
        return redirect('resume_skills', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': skill,
        'resume': resume
    })

@login_required
def projects(request, resume_slug):
    """Step to add projects to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    projects = resume.project_set.all()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.resume = resume
            project.save()
            messages.success(request, 'Project added successfully.')
            return redirect('resume_projects', resume_slug=resume.slug)
    else:
        form = ProjectForm()

    return render(request, 'resumes/projects.html', {
        'form': form,
        'projects': projects,
        'resume': resume,
        'section': 'projects'
    })

@login_required
def delete_project(request, resume_slug, project_id):
    """Delete a specific project entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    project = get_object_or_404(Project, id=project_id, resume=resume)
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project removed successfully.')
        return redirect('resume_projects', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': project,
        'resume': resume
    })

@login_required
def certifications(request, resume_slug):
    """Step to add certifications to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    certifications = resume.certification_set.all()

    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.resume = resume
            certification.save()
            messages.success(request, 'Certification added successfully.')
            return redirect('resume_certifications', resume_slug=resume.slug)
    else:
        form = CertificationForm()

    return render(request, 'resumes/certifications.html', {
        'form': form,
        'certifications': certifications,
        'resume': resume,
        'section': 'certifications'
    })

@login_required
def delete_certification(request, resume_slug, certification_id):
    """Delete a specific certification entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    certification = get_object_or_404(Certification, id=certification_id, resume=resume)
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, 'Certification removed successfully.')
        return redirect('resume_certifications', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': certification,
        'resume': resume
    })

@login_required
def languages(request, resume_slug):
    """Step to add languages to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    languages = resume.language_set.all()

    if request.method == 'POST':
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.resume = resume
            language.save()
            messages.success(request, 'Language added successfully.')
            return redirect('resume_languages', resume_slug=resume.slug)
    else:
        form = LanguageForm()

    return render(request, 'resumes/languages.html', {
        'form': form,
        'languages': languages,
        'resume': resume,
        'section': 'languages'
    })

@login_required
def delete_language(request, resume_slug, language_id):
    """Delete a specific language entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    language = get_object_or_404(Language, id=language_id, resume=resume)
    
    if request.method == 'POST':
        language.delete()
        messages.success(request, 'Language removed successfully.')
        return redirect('resume_languages', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': language,
        'resume': resume
    })

@login_required
def references(request, resume_slug):
    """Step to add references to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    references = resume.references.all()

    if request.method == 'POST':
        form = ReferenceForm(request.POST)
        if form.is_valid():
            reference = form.save(commit=False)
            reference.resume = resume
            reference.save()
            messages.success(request, 'Reference added successfully.')
            return redirect('resume_references', resume_slug=resume.slug)
    else:
        form = ReferenceForm()

    return render(request, 'resumes/references.html', {
        'form': form,
        'references': references,
        'resume': resume,
        'section': 'references'
    })

@login_required
def delete_reference(request, resume_slug, reference_id):
    """Delete a specific reference entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    reference = get_object_or_404(Reference, id=reference_id, resume=resume)
    
    if request.method == 'POST':
        reference.delete()
        messages.success(request, 'Reference removed successfully.')
        return redirect('resume_references', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': reference,
        'resume': resume
    })

@login_required
def custom_sections(request, resume_slug):
    """Step to add custom sections to the resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    custom_sections = resume.custom_sections.all()

    if request.method == 'POST':
        form = CustomSectionForm(request.POST)
        if form.is_valid():
            custom_section = form.save(commit=False)
            custom_section.resume = resume
            custom_section.save()
            messages.success(request, 'Custom section added successfully.')
            return redirect('resume_custom_sections', resume_slug=resume.slug)
    else:
        form = CustomSectionForm()

    return render(request, 'resumes/custom_sections.html', {
        'form': form,
        'custom_sections': custom_sections,
        'resume': resume,
        'section': 'custom_sections'
    })

@login_required
def delete_custom_section(request, resume_slug, custom_section_id):
    """Delete a specific custom section entry"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    custom_section = get_object_or_404(CustomSection, id=custom_section_id, resume=resume)
    
    if request.method == 'POST':
        custom_section.delete()
        messages.success(request, 'Custom section removed successfully.')
        return redirect('resume_custom_sections', resume_slug=resume.slug)
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': custom_section,
        'resume': resume
    })

def resume_preview(request, resume_slug):
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    domain = request.get_host()

    # Fetch all related data
    personal_info = resume.personalinfo if hasattr(resume, 'personalinfo') else None
    work_experiences = resume.workexperience_set.all()
    education_entries = resume.education_set.all()
    skills = resume.skill_set.all()
    projects = resume.project_set.all()
    certifications = resume.certification_set.all()
    languages = resume.language_set.all()
    references = resume.references.all()
    custom_sections = resume.custom_sections.all()

    # Mark resume as complete when preview is accessed
    resume.is_complete = True
    resume.save()

    # Create context dictionary
    context = {
        'resume': resume,
        'personal_info': personal_info,
        'work_experiences': work_experiences,
        'education_entries': education_entries,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'languages': languages,
        'references': references,
        'custom_sections': custom_sections,
        'section': 'preview',
        'domain': domain,
    }
    
    if resume.template:
        # Parse and render the dynamic template
        template_content = Template(resume.template.html_content)
        rendered_content = template_content.render(Context(context))
        context['rendered_template'] = rendered_content
        
    return render(request, 'resumes/preview.html', context)

def public_resume_view(request, slug):
    resume = get_object_or_404(Resume, slug=slug, is_complete=True)
    
    # Fetch all related data
    personal_info = resume.personalinfo if hasattr(resume, 'personalinfo') else None
    work_experiences = resume.workexperience_set.all()
    education_entries = resume.education_set.all()
    skills = resume.skill_set.all()
    projects = resume.project_set.all()
    certifications = resume.certification_set.all()
    languages = resume.language_set.all()
    references = resume.references.all()
    custom_sections = resume.custom_sections.all()

    context = {
        'resume': resume,
        'personal_info': personal_info,
        'work_experiences': work_experiences,
        'education_entries': education_entries,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'languages': languages,
        'references': references,
        'custom_sections': custom_sections
    }

    if resume.template:
        # Parse and render the dynamic template
        template_content = Template(resume.template.html_content)
        rendered_content = template_content.render(Context(context))
        context['rendered_template'] = rendered_content

    return render(request, 'resumes/public_resume.html', context)


@login_required
def resume_list(request):
    """List all resumes created by the user"""
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'resumes/resume_list.html', {
        'resumes': resumes,
        'section': 'resume_list'
    })

@login_required
def edit_resume(request, resume_slug):
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    # Map section names to their corresponding forms and models
    SECTION_MAPPING = {
        'personal_info': (PersonalInfoForm, 'personalinfo'),  # One-to-one relationship
        'work_experience': (WorkExperienceForm, 'workexperience_set'),
        'education': (EducationForm, 'education_set'),
        'skills': (SkillForm, 'skill_set'),
        'projects': (ProjectForm, 'project_set'),
        'certifications': (CertificationForm, 'certification_set'),
        'languages': (LanguageForm, 'language_set'),
        'references': (ReferenceForm, 'references'),
        'custom_sections': (CustomSectionForm, 'custom_sections')
    }

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        action = request.POST.get('action')
        section = request.POST.get('section')
        
        try:
            if action == 'update':
                if section == 'title':
                    form = ResumeForm(request.POST, instance=resume)
                    if form.is_valid():
                        form.save()
                        return JsonResponse({'success': True})
                
                form_class, model_attr = SECTION_MAPPING.get(section)
                instance_id = request.POST.get('id')
                instance = getattr(resume, model_attr).filter(id=instance_id).first() if instance_id else None
                form = form_class(request.POST, instance=instance)
                
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.resume = resume
                    obj.save()
                    return JsonResponse({'success': True})
                return JsonResponse({'success': False, 'errors': form.errors})
            
            elif action == 'delete':
                instance_id = request.POST.get('id')
                _, model_attr = SECTION_MAPPING.get(section)
                getattr(resume, model_attr).filter(id=instance_id).delete()
                return JsonResponse({'success': True})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    # Prepare context for GET request
    context = {
        'resume': resume,
        'sections': {}
    }
    
    for section, (form_class, model_attr) in SECTION_MAPPING.items():
        if section == 'personal_info':
            # Handle one-to-one relationship
            instance = getattr(resume, model_attr, None)
            context['sections'][section] = {
                'form': form_class(instance=instance) if instance else form_class(),
                'items': [instance] if instance else []
            }
        else:
            # Handle one-to-many relationships
            context['sections'][section] = {
                'form': form_class(),
                'items': getattr(resume, model_attr).all()
            }

    return render(request, 'resumes/edit_resume.html', context)



@login_required
def delete_resume(request, resume_slug):
    """Delete an entire resume"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully.')
        return redirect('resume_list')
    
    return render(request, 'resumes/confirm_delete.html', {
        'object': resume
    })



@login_required
def initialize_template_payment(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id)
    
    # Initialize payment with Paystack
    paystack_secret = settings.PAYSTACK_SECRET_KEY
    url = "https://api.paystack.co/transaction/initialize"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": request.user.email,
        "amount": int(template.price * 100),  # Convert to kobo
        "currency": "NGN",
        "callback_url": request.build_absolute_uri(reverse('payment_webhook')),
        "metadata": {
            "template_id": template_id,
            "user_id": request.user.id
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return JsonResponse({
            "status": "success",
            "data": response.json()["data"]
        })
    
    return JsonResponse({
        "status": "error",
        "message": "Failed to initialize payment"
    }, status=400)

@csrf_exempt
def payment_webhook(request):
    if request.method == 'POST':
        # Handle webhook POST from Paystack
        payload = json.loads(request.body)
        reference = payload.get('reference')
    else:
        # Handle GET redirect from payment page
        reference = request.GET.get('reference')
    
    if not reference:
        return JsonResponse({'status': 'error', 'message': 'No reference provided'})
    
    # Verify the payment with Paystack
    paystack_secret = settings.PAYSTACK_SECRET_KEY
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['status'] == 'success':
            # Get metadata from the transaction
            metadata = response_data['data']['metadata']
            template_id = metadata.get('template_id')
            user_id = metadata.get('user_id')
            
            # Create UserTemplate record
            template = ResumeTemplate.objects.get(id=template_id)
            user = User.objects.get(id=user_id)
            UserTemplate.objects.create(
                user=user,
                template=template,
                payment_reference=reference
            )
            
            # Redirect to template selection with success message
            return redirect(f"{reverse('template_selection')}?payment_status=success")
    
    # Redirect with error message if verification fails
    return redirect(f"{reverse('template_selection')}?payment_status=failed")



def verify_payment(request, reference):
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    
    response = requests.get(
        f'https://api.paystack.co/transaction/verify/{reference}',
        headers=headers
    )
    
    if response.json()['data']['status'] == 'success':
        metadata = response.json()['data']['metadata']
        UserTemplate.objects.create(
            user_id=metadata['user_id'],
            template_id=metadata['template_id'],
            payment_reference=reference
        )
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failed'})


@login_required
def template_selection(request):
    templates = ResumeTemplate.objects.filter(is_active=True)
    user_templates = ResumeTemplate.objects.filter(
        id__in=UserTemplate.objects.filter(user=request.user).values_list('template_id', flat=True)
    )
    
    context = {
        'templates': templates,
        'user_templates': user_templates
    }
    return render(request, 'resumes/template_selection.html', context)

@login_required
def select_template(request, template_id):
    resume_slug = request.GET.get('resume_slug')
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    if template_id == 'default':
        resume.template = None
        resume.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Default template applied successfully'
        })
    
    template = get_object_or_404(ResumeTemplate, id=template_id)
    
    # Check if user has access to this template
    has_access = template.is_free or UserTemplate.objects.filter(
        user=request.user, 
        template=template
    ).exists()
    
    if has_access:
        resume.template = template
        resume.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Template applied successfully',
            'template_name': template.name
        })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Template access denied'
    }, status=403)


@login_required
def preview_template(request, template_id):
    template = get_object_or_404(ResumeTemplate, id=template_id)
    resume_slug = request.GET.get('resume_slug')
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    # Fetch all resume data
    personal_info = resume.personalinfo if hasattr(resume, 'personalinfo') else None
    work_experiences = resume.workexperience_set.all()
    education_entries = resume.education_set.all()
    skills = resume.skill_set.all()
    projects = resume.project_set.all()
    certifications = resume.certification_set.all()
    languages = resume.language_set.all()
    references = resume.references.all()
    custom_sections = resume.custom_sections.all()
    
    context = {
        'resume': resume,
        'personal_info': personal_info,
        'work_experiences': work_experiences,
        'education_entries': education_entries,
        'skills': skills,
        'projects': projects,
        'certifications': certifications,
        'languages': languages,
        'references': references,
        'custom_sections': custom_sections,
        'preview_mode': True,
        'template': template
    }
    
    # Render the template content
    template_content = Template(template.html_content)
    rendered_content = template_content.render(Context(context))
    context['rendered_template'] = rendered_content
    
    return render(request, 'resumes/preview_template.html', context)


@login_required
def download_resume_pdf(request, resume_slug):
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
    # Check if user has free download from template purchase
    has_free_download = (
        resume.template and 
        UserTemplate.objects.filter(
            user=request.user, 
            template=resume.template
        ).exists() and
        not PDFDownload.objects.filter(
            user=request.user,
            resume=resume,
            template=resume.template,
            is_free=True
        ).exists()
    )
    
    if has_free_download:
        return generate_pdf(request, resume, is_free=True)
    
    # Check if payment is required
    if request.GET.get('payment_verified'):
        return generate_pdf(request, resume)
    
    # Initialize payment for PDF download
    return initialize_pdf_payment(request, resume)


def get_resume_context(resume):
    context = {
        'resume': resume,
        'personal_info': resume.personalinfo if hasattr(resume, 'personalinfo') else None,
        'work_experiences': resume.workexperience_set.all(),
        'education_entries': resume.education_set.all(),
        'skills': resume.skill_set.all(),
        'projects': resume.project_set.all(),
        'certifications': resume.certification_set.all(),
        'languages': resume.language_set.all(),
        'references': resume.references.all(),
        'custom_sections': resume.custom_sections.all(),
    }
    
    if resume.template:
        template_content = Template(resume.template.html_content)
        rendered_content = template_content.render(Context(context))
        context['rendered_template'] = rendered_content
    
    return context


def generate_pdf(resume, request):
    # Get the template's CSS file path
    template_css = None
    if resume.template and resume.template.css_file:
        template_css = resume.template.css_file.path

    # Base CSS for consistent styling
    base_css = '''
        @page {
            size: letter;
            margin: 0;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
        }
        
        img {
            max-width: 100%;
            height: auto;
        }
        
        .resume-container {
            padding: 40px;
        }
    '''

    # Create context with all resume data
    context = {
        'resume': resume,
        'personal_info': resume.personalinfo if hasattr(resume, 'personalinfo') else None,
        'work_experiences': resume.workexperience_set.all(),
        'education_entries': resume.education_set.all(),
        'skills': resume.skill_set.all(),
        'projects': resume.project_set.all(),
        'certifications': resume.certification_set.all(),
        'languages': resume.language_set.all(),
        'references': resume.references.all(),
        'custom_sections': resume.custom_sections.all(),
        'pdf_mode': True,  # Flag to handle PDF-specific styling
        'request': request,  # Add request to context for URL handling
        'domain': request.get_host(),
    }

    # Render the HTML content using the same template as the preview
    if resume.template:
        template_content = Template(resume.template.html_content)
        html_string = template_content.render(Context(context))
    else:
        html_string = render_to_string('resumes/pdf_template.html', context)

    # Collect all stylesheets
    stylesheets = [CSS(string=base_css)]
    
    # Add template-specific CSS if it exists
    if template_css and os.path.exists(template_css):
        stylesheets.append(CSS(filename=template_css))
    
    # Add any additional static CSS files
    static_css_path = os.path.join(settings.STATIC_ROOT, 'css/resume-pdf.css')
    if os.path.exists(static_css_path):
        stylesheets.append(CSS(filename=static_css_path))

    # Generate PDF
    pdf = HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(
        stylesheets=stylesheets,
        presentational_hints=True
    )

    return pdf



@login_required
def initialize_pdf_payment(request, resume_slug):
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    site_settings = SiteSettings.objects.first()
    
    # Initialize payment with Paystack
    paystack_secret = settings.PAYSTACK_SECRET_KEY
    url = "https://api.paystack.co/transaction/initialize"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret}",
        "Content-Type": "application/json"
    }
    
    data = {
        "email": request.user.email,
        "amount": int(site_settings.pdf_download_price * 100),  # Convert to kobo
        "currency": "NGN",
        "callback_url": request.build_absolute_uri(
            reverse('pdf_payment_verify', kwargs={'resume_slug': resume_slug})
        ),
        "metadata": {
            "resume_slug": resume_slug,
            "user_id": request.user.id,
            "type": "pdf_download"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return JsonResponse({
            "status": "success",
            "data": response.json()["data"]
        })
    
    return JsonResponse({
        "status": "error",
        "message": "Failed to initialize payment"
    }, status=400)

@csrf_exempt
def verify_pdf_payment(request, resume_slug):
    if request.method == 'POST':
        payload = json.loads(request.body)
        reference = payload.get('reference')
    else:
        reference = request.GET.get('reference')
    
    if not reference:
        return JsonResponse({'status': 'error', 'message': 'No reference provided'})
    
    # Verify the payment with Paystack
    paystack_secret = settings.PAYSTACK_SECRET_KEY
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['status'] == 'success':
            # Get metadata from the transaction
            metadata = response_data['data']['metadata']
            resume_slug = metadata.get('resume_slug')
            
            # Redirect to PDF download with verification
            return redirect(
                f"{reverse('download_pdf', kwargs={'resume_slug': resume_slug})}?payment_verified=true&reference={reference}"
            )
    
    # Redirect with error message if verification fails
    return redirect(f"{reverse('resume_preview', kwargs={'resume_slug': resume_slug})}?payment_status=failed")
