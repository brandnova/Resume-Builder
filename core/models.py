from django.db import models

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100)
    site_description = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)
    
    # SEO Fields
    meta_keywords = models.TextField(help_text="Comma-separated keywords")
    meta_description = models.TextField()
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Pricing
    pdf_download_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Price for downloading resume as PDF"
    )
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return self.site_name