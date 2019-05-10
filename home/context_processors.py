from home.models import SiteConfig


def sitemanage_context(request):
    site_data = {}
    if SiteConfig.objects.filter(id=1).exists():
        site_config = SiteConfig.objects.get(id=1)
        print('dddddddddddd', site_config.get_favicon())
        site_data = {
            "site_description": site_config.site_desc,
            "meta_description": site_config.meta_description,
            "site_owner_name": site_config.owner_name,
            "site_favicon": site_config.get_favicon(),
            "site_logo": site_config.get_logo(),
            "website_name": site_config.site_name,
            "phone_number": site_config.phone_number,
            "email": site_config.email,
            "address": site_config.address,
            "fb_link": site_config.fb_link,
            "youtube_link": site_config.youtube_link,
            "linkedin_link": site_config.linkedin_link,
            "copyright": site_config.copyright,
            "twitter_link": site_config.twitter_link
        }
    return site_data
