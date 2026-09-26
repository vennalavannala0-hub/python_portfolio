from .models import SiteProfile


def site_profile(request):
    return {"site_profile": SiteProfile.get_solo()}
