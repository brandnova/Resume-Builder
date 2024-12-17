from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Resume, PersonalInfo, WorkExperience, Education, Skill, 
    Project, Certification, Language, Reference, CustomSection, ResumeTemplate, UserTemplate, PDFDownload
)

# Inline models for easier management within the Resume admin
class PersonalInfoInline(admin.StackedInline):
    model = PersonalInfo
    extra = 0

class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1

class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

class SkillInline(admin.TabularInline):
    model = Skill

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 1

class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

class LanguageInline(admin.TabularInline):
    model = Language
    extra = 1

class ReferenceInline(admin.TabularInline):
    model = Reference
    extra = 1

class CustomSectionInline(admin.StackedInline):
    model = CustomSection
    extra = 0

# Main Resume admin configuration
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_complete', 'created_at', 'updated_at')
    list_filter = ('is_complete', 'created_at', 'updated_at')
    search_fields = ('title', 'user__username')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [
        PersonalInfoInline,
        WorkExperienceInline,
        EducationInline,
        SkillInline,
        ProjectInline,
        CertificationInline,
        LanguageInline,
        ReferenceInline,
        CustomSectionInline,
    ]

# Individual model admin configurations
@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'location', 'resume')
    search_fields = ('full_name', 'email', 'location')

@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'location', 'start_date', 'end_date', 'resume')
    list_filter = ('start_date', 'end_date')
    search_fields = ('job_title', 'company', 'location')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'location', 'start_date', 'end_date', 'resume')
    list_filter = ('start_date', 'end_date')
    search_fields = ('degree', 'institution', 'location')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'resume')
    search_fields = ('name', 'level')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'resume')
    search_fields = ('name', 'technologies')
    list_filter = ('start_date', 'end_date')

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'date_obtained', 'expiration_date', 'resume')
    list_filter = ('date_obtained', 'expiration_date')
    search_fields = ('name', 'organization')

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'proficiency', 'resume')
    search_fields = ('name', 'proficiency')

@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('reference_name', 'position', 'organization', 'email', 'phone', 'resume')
    search_fields = ('reference_name', 'organization', 'email')

@admin.register(CustomSection)
class CustomSectionAdmin(admin.ModelAdmin):
    list_display = ('section_name', 'resume')
    search_fields = ('section_name',)

@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    list_filter = ['is_active', 'price']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at'] 

@admin.register(UserTemplate)
class UserTemplateAdmin(admin.ModelAdmin):
    list_display = ['user', 'template', 'purchased_at']
    list_filter = ['purchased_at']
    search_fields = ['user__username', 'template__name']


admin.site.register(PDFDownload)