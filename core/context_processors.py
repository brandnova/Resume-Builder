from .models import SiteSettings
from resumes.models import ResumeTemplate

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
        templates = ResumeTemplate.objects.filter(is_active=True)[:6]
        return {
            'site_settings': settings,
            'featured_templates': templates
        }
    except:
        return {
            'site_settings': None,
            'featured_templates': []
        }
