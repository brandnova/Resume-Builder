from .models import SiteSettings
from resumes.models import ResumeTemplate

def site_settings(request):
    try:
        settings = SiteSettings.objects.first()
        # Fetch random active templates
        templates = ResumeTemplate.objects.filter(is_active=True).order_by('?')
        return {
            'site_settings': settings,
            'featured_templates': templates
        }
    except:
        return {
            'site_settings': None,
            'featured_templates': []
        }
