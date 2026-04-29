# django-visitor-stats

Reusable Django app: page-view tracking with 30-minute session deduplication, optional IP geolocation (ip-api.com), user-agent parsing, and a dashboard with charts and a Leaflet map.

## Clone and develop

```bash
git clone https://github.com/marobo/visitor_stats.git
cd <repo>
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Install

**Standalone repo** (when this app is its own Git repository):

```bash
pip install "django-visitor-stats @ git+https://github.com/marobo/visitor_stats.git@v0.1.0"
```

**Monorepo subdirectory** (install only the `visitor_stats/` folder from a parent project):

```bash
pip install "django-visitor-stats @ git+https://github.com/marobo/visitor_stats.git@v0.1.0#subdirectory=visitor_stats"
```

**Local editable** (development):

```bash
pip install -e /path/to/visitor_stats
```

## Configure

1. Add to `INSTALLED_APPS`:

   ```python
   INSTALLED_APPS = [
       # ...
       'visitor_stats',
   ]
   ```

2. Include URLs (path is up to you):

   ```python
   urlpatterns = [
       path('stats/', include('visitor_stats.urls')),
   ]
   ```

3. Run migrations:

   ```bash
   python manage.py migrate visitor_stats
   ```

4. Record visits — pick one:

   - **Per view:** `from visitor_stats.views import track_visitor` and call `track_visitor(request)` in views you care about.
   - **Global:** add middleware after `SessionMiddleware`:

     ```python
     MIDDLEWARE = [
         # ...
         'visitor_stats.middleware.VisitorTrackingMiddleware',
     ]
     ```

     Do not combine duplicate calls on the same route without understanding session deduplication (same request may run both; dedupe usually prevents double inserts).

### Optional settings

| Setting | Default | Purpose |
|--------|---------|---------|
| `VISITOR_STATS_BASE_TEMPLATE` | `visitor_stats/base.html` | Template the dashboard extends (set to your site `base.html` for consistent chrome). |
| `VISITOR_STATS_HOME_URL_NAME` | `None` | If set (e.g. `'home'`), the dashboard shows a “Back” link to that URL name. |
| `VISITOR_STATS_TEMPLATE` | `visitor_stats/visitor_stats.html` | Override the dashboard template. |
| `VISITOR_STATS_URL_PREFIX` | `'/stats/'` | Used by middleware to skip tracking on the stats pages (match your URL mount). |
| `VISITOR_TRACKING_ENABLED` | `True` | Set `False` to disable middleware tracking. |
| `VISITOR_TRACKING_EXCLUDE_PREFIXES` | `()` | Extra path prefixes to skip (e.g. `('/api/',)`). |

Geolocation uses the public `ip-api.com` HTTP endpoint; respect their terms and rate limits. Local IPs are not geolocated.

## License

[MIT](LICENSE)
