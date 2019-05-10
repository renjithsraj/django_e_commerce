from django.db import models
from django.urls import reverse
from django.utils.translation import  ugettext_lazy as _
from imagekit.models import ProcessedImageField
from django.core.exceptions import  ValidationError


# Create your models here.

class SiteConfig(models.Model):
    site_name = models.CharField(max_length=200, null=False, blank=False)
    owner_name = models.CharField(_("Owner Name"), max_length=50)
    site_desc = models.CharField(max_length=200, null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)
    logo = ProcessedImageField(upload_to='images/site',
                                         format='JPEG',
                                         options={'quality': 60}, null=True, blank=True, verbose_name="Logo(height:25px,width:33px)")
    fav_icon = ProcessedImageField(upload_to='images/site',
                                         format='JPEG',
                                         options={'quality': 60}, null=True, blank=True, verbose_name="Favicon(height:16px,width:19px)")
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    fb_link = models.URLField(null=True, blank=True)
    youtube_link = models.URLField(null=True, blank=True)
    twitter_link = models.URLField(null=True, blank=True)
    linkedin_link = models.URLField(null=True, blank=True)
    copyright = models.CharField(_("Copy right"), max_length=50)

    def save(self, *args, **kwargs):
        if SiteConfig.objects.exists() and not self.pk:
            # if you'll not check for self.pk
            # then error will also raised in update of exists model
            raise ValidationError(
                'There is can be only one SiteConfig instance')
        return super(SiteConfig, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("SiteConfig")
        verbose_name_plural = _("SiteConfigs")

    def __str__(self):
        return self.site_name

    def get_logo(self):
        if not self.logo:
            return "/static/site_config/no_image.jpeg"
        return  self.logo.url
    
    def get_favicon(self):
        if not self.fav_icon:
            return "/static/site_config/favicon.png"
        return self.fav_icon.url



    def get_absolute_url(self):
        return reverse("siteconnfig_detail", kwargs={"pk": self.pk})
