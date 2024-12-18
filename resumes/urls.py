from django.urls import path
from . import views

urlpatterns = [
     # Resume Creation Process
     path('create/', views.create_resume, name='create_resume'),
     path('<slug:resume_slug>/personal-info/', views.personal_info, name='resume_personal_info'),
          # Work Experience Routes
     path('<slug:resume_slug>/work-experience/', views.work_experience, name='resume_work_experience'),
     path('<slug:resume_slug>/work-experience/delete/<int:work_exp_id>/', 
          views.delete_work_experience, name='delete_work_experience'),
          # Education Routes
     path('<slug:resume_slug>/education/', views.education, name='resume_education'),
     path('<slug:resume_slug>/education/delete/<int:education_id>/', 
          views.delete_education, name='delete_education'),
          # Skills Routes
     path('<slug:resume_slug>/skills/', views.skills, name='resume_skills'),
     path('<slug:resume_slug>/skills/delete/<int:skill_id>/', 
          views.delete_skill, name='delete_skill'),
          # Projects Routes
     path('<slug:resume_slug>/projects/', views.projects, name='resume_projects'),
     path('<slug:resume_slug>/projects/delete/<int:project_id>/', 
          views.delete_project, name='delete_project'),
          # Certifications Routes
     path('<slug:resume_slug>/certifications/', views.certifications, name='resume_certifications'),
     path('<slug:resume_slug>/certifications/delete/<int:certification_id>/', 
          views.delete_certification, name='delete_certification'),

     # Languages Routes
     path('<slug:resume_slug>/languages/', views.languages, name='resume_languages'),
     path('<slug:resume_slug>/languages/delete/<int:language_id>/', 
          views.delete_language, name='delete_language'),

     # References Routes
     path('<slug:resume_slug>/references/', views.references, name='resume_references'),
     path('<slug:resume_slug>/references/delete/<int:reference_id>/', 
          views.delete_reference, name='delete_reference'),

     # Custom Sections Routes
     path('<slug:resume_slug>/custom-sections/', views.custom_sections, name='resume_custom_sections'),
     path('<slug:resume_slug>/custom-sections/delete/<int:custom_section_id>/', 
          views.delete_custom_section, name='delete_custom_section'),
     
     # Resume Preview and Management
     path('<slug:resume_slug>/preview/', views.resume_preview, name='resume_preview'),
     path('list/', views.resume_list, name='resume_list'),
     path('<slug:resume_slug>/edit/', views.edit_resume, name='edit_resume'),
     path('<slug:resume_slug>/delete/', views.delete_resume, name='delete_resume'),
     
     # Public Resume View
     path('view/<slug:slug>/', views.public_resume_view, name='public_resume_view'),

     # Template Management Routes
     path('templates/', views.template_selection, name='template_selection'),
     path('select-template/<str:template_id>/', views.select_template, name='select_template'),
     path('preview-template/<int:template_id>/', views.preview_template, name='preview_template'),
     path('initialize-payment/<int:template_id>/', views.initialize_template_payment, name='initialize_payment'),
     path('payment-webhook/', views.payment_webhook, name='payment_webhook'),
     path('verify-payment/<str:reference>/', views.verify_payment, name='verify_payment'),

     # PDF Management Routes
     path('resumes/<str:resume_slug>/generate-pdf/', views.generate_pdf, name='generate_pdf'),
     path('<slug:resume_slug>/download-pdf/', views.download_resume_pdf, name='download_pdf'),
     path('<slug:resume_slug>/initialize-pdf-payment/', views.initialize_pdf_payment, name='initialize_pdf_payment'),
     path('<slug:resume_slug>/verify-pdf-payment/', views.verify_pdf_payment, name='pdf_payment_verify'),

     # DOCX Management Routes
     path('<str:resume_slug>/initialize-docx-payment/', views.initialize_docx_payment, name='initialize_docx_payment'),
     path('<str:resume_slug>/generate-docx/', views.generate_docx, name='generate_docx'),
     path('<str:resume_slug>/verify-docx-payment/', views.verify_docx_payment, name='verify_docx_payment'),


]