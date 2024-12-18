from django.contrib import admin
from .models import SiteSettings

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email')
    fieldsets = (
        ('General Information', {
            'fields': (
                'site_name',
                'site_description',
                'contact_email',
                'contact_phone',
                'address',
            )
        }),
        ('SEO', {
            'fields': (
                'meta_keywords',
                'meta_description',
            ),
            'classes': ['collapse'],  # Collapse this section by default
        }),
        ('Social Media', {
            'fields': (
                'facebook_url',
                'twitter_url',
                'linkedin_url',
            ),
            'classes': ['collapse'],  # Collapse this section by default
        }),
        ('Pricing', {
            'fields': (
                'pdf_download_price',
                'docx_download_price',
            ),
            'classes': ['collapse'],  # Collapse this section by default
        }),
    )

admin.site.register(SiteSettings, SiteSettingsAdmin)