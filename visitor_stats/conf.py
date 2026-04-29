from django.conf import settings


def base_template():
    return getattr(
        settings,
        'VISITOR_STATS_BASE_TEMPLATE',
        'visitor_stats/base.html',
    )


def home_url_name():
    return getattr(settings, 'VISITOR_STATS_HOME_URL_NAME', None)
