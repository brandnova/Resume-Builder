from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from .models import (
    Resume, PersonalInfo, WorkExperience, Education, 
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

# Update existing resume_preview and public_resume_view to include new sections
@login_required
def resume_preview(request, resume_slug):
    """Preview the entire resume with all sections"""
    resume = get_object_or_404(Resume, slug=resume_slug, user=request.user)
    
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

    return render(request, 'resumes/preview.html', {
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
        'section': 'preview'
    })

@login_required
def resume_list(request):
    """List all resumes created by the user"""
    resumes = Resume.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'resumes/resume_list.html', {
        'resumes': resumes,
        'section': 'resume_list'
    })

def public_resume_view(request, slug):
    """Publicly accessible resume view with all sections"""
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

    return render(request, 'resumes/public_resume.html', {
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
    })

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
