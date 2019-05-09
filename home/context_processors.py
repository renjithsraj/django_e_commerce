from home.models import SiteConfig


def sitemanage_context(request):
    site_data = {
        "site_description": "",
        "meta_description": "",
        "site_owner_name": "",
        "site_favicon": "",
        "site_logo": "",
        "website_name": "",
        "phone_number": "",
        "email": "",
        "address": "",
        "fb_link": "",
        "youtube_link": "",
        "linkedin_link": "",
        "copyright": "",
        "twitter_link": ""
    }
    return site_data
