from django.conf import settings

from .views import track_visitor


def _exclude_prefixes():
    default = ['/admin/', '/static/']
    extra = getattr(settings, 'VISITOR_TRACKING_EXCLUDE_PREFIXES', ())
    return tuple(default) + tuple(extra)


def _should_track(request):
    path = request.path
    for prefix in _exclude_prefixes():
        if path.startswith(prefix):
            return False

    media_url = getattr(settings, 'MEDIA_URL', '') or ''
    if media_url:
        m = media_url.rstrip('/')
        if m and (path == m or path.startswith(m + '/')):
            return False

    raw = getattr(settings, 'VISITOR_STATS_URL_PREFIX', '/stats/')
    p = raw.rstrip('/') or '/stats'
    if path == p or path.startswith(p + '/'):
        return False

    return True


class VisitorTrackingMiddleware:
    """Call track_visitor() for each request (requires SessionMiddleware before this)."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, 'VISITOR_TRACKING_ENABLED', True) and _should_track(request):
            track_visitor(request)
        return self.get_response(request)
