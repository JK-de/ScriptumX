# Template overlay (operator-specific legal text)

Django loads templates from `DJANGO_TEMPLATE_OVERLAY` (default `/data/templates`)
before the packaged app templates. Put personalized files there, for example:

```
/data/templates/web/impressum.html
/data/templates/web/datenschutz.html
```

The Docker volume `scriptumx-data` mounts at `/data`, so overlays survive rebuilds
and are not part of the git repository. Packaged templates keep placeholders only.
