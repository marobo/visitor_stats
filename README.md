# django-visitor-stats

Reusable Django app: page-view tracking with 30-minute session deduplication, optional IP geolocation (ip-api.com), user-agent parsing, and a dashboard with charts and a Leaflet map.

**Requirements:** Python 3.10+ and Django 4.2+.

## Clone and develop

```bash
git clone git@github.com:marobo/visitor_stats.git
cd visitor_stats
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .
```

## Install

**This repository** (`pyproject.toml` at the repo root): install from the root URL — **do not** use `#subdirectory=…` (that is only when the installable project lives in a subfolder of a larger repo).

```bash
pip install "django-visitor-stats @ git+https://github.com/marobo/visitor_stats.git@v0.1.0"
```

**Monorepo** (when `pyproject.toml` for this app is under a path like `packages/django-visitor-stats/` inside another repository):

```bash
pip install "django-visitor-stats @ git+https://github.com/<owner>/<monorepo>.git@v0.1.0#subdirectory=packages/django-visitor-stats"
```

The `#subdirectory=` value must be the folder that **contains** `pyproject.toml`, not the inner Python package directory alone.

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

   The dashboard view is named `visitor_stats`, so you can link to it with `{% url 'visitor_stats' %}` or `reverse('visitor_stats')`.

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

     If you enable the middleware, you generally don't need to also call `track_visitor()` from your views. Both will fire on the same request, but the 30-minute session-based dedupe normally suppresses the second insert.

5. View the dashboard. Run the server and open the URL where you mounted the app, e.g. <http://localhost:8000/stats/>.

   `Visitor` records are also browsable in the Django admin at `/admin/`.

## Optional settings

| Setting | Default | Purpose |
|--------|---------|---------|
| `VISITOR_STATS_BASE_TEMPLATE` | `visitor_stats/base.html` | Template the dashboard extends (set to your site `base.html` for consistent chrome). |
| `VISITOR_STATS_HOME_URL_NAME` | `None` | If set (e.g. `'home'`), the dashboard shows a “Back” link to that URL name. |
| `VISITOR_STATS_TEMPLATE` | `visitor_stats/visitor_stats.html` | Override the dashboard template. |
| `VISITOR_STATS_URL_PREFIX` | `'/stats/'` | Path prefix where the dashboard is mounted; the middleware uses it to skip self-tracking. Set it to the same prefix you pass to `include('visitor_stats.urls')`. |
| `VISITOR_TRACKING_ENABLED` | `True` | Set `False` to disable middleware tracking. |
| `VISITOR_TRACKING_EXCLUDE_PREFIXES` | `()` | Extra path prefixes to skip (e.g. `('/api/',)`). The middleware **always** also skips `/admin/`, `/static/`, `MEDIA_URL`, and the dashboard prefix. |

## Notes

**Behind a proxy or Cloudflare.** Client IP is read from `HTTP_CF_CONNECTING_IP`, then `HTTP_X_REAL_IP`, then the first entry of `HTTP_X_FORWARDED_FOR`, falling back to `REMOTE_ADDR`. These headers are spoofable, so make sure your proxy strips/overwrites them on inbound requests.

**Geolocation.** Local IPs (`127.0.0.1`, `::1`, `localhost`) are not geolocated. Other IPs are looked up against the public `ip-api.com` HTTP endpoint, which is rate-limited (~45 requests/minute per source IP) and unencrypted; respect their terms. Failed or rate-limited lookups simply leave `country`/`city`/`latitude`/`longitude` blank.

## License

[MIT](LICENSE)
