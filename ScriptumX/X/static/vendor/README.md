# Vendored front-end assets (H18)

Kept Bootstrap **3** (crispy-bootstrap3 + existing markup). Bootstrap 5 migration is deferred.

| Asset | Version | Path | Source |
|-------|---------|------|--------|
| Bootstrap CSS/JS | 3.3.6 | `X/static/X/content/bootstrap.min.css`, `X/static/X/scripts/bootstrap.min.js` | Already in-tree (was partially CDN for JS) |
| jQuery | 2.2.4 | `X/static/vendor/jquery/jquery-2.2.4.min.js` | jsDelivr `npm/jquery@2.2.4` |
| Font Awesome | 4.7.0 | `X/static/vendor/font-awesome/` | jsDelivr `npm/font-awesome@4.7.0` |

Templates now load these via `{% static %}` instead of maxcdn / ajax.googleapis CDNs.
