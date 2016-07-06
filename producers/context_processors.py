from django.conf import settings


# Things that we want to be available in the context of every page.

def api_keys(request):
    return {
        'MAPBOX_API_KEY': settings.MAPBOX_API_KEY,
        #'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }

def url_name(request):
    """
    So we can test things in the templates based on the current named URL.
    """
    url_name = False
    if request.resolver_match:
        url_name = request.resolver_match.url_name
    return {'url_name': url_name}


