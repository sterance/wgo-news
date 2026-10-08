"""``{% vite_assets "index.html" %}``: the <link>/<script> tags for a Vite build entry.

Reads the manifest Vite writes with ``build.manifest`` (``npm run build:django``)
so the hashed asset file names never need hard-coding.
"""

import json
from functools import lru_cache
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()


def manifest_path() -> Path:
    return Path(settings.FRONTEND_BUILD_DIR) / ".vite" / "manifest.json"


def _read_manifest(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


_read_manifest_cached = lru_cache(maxsize=None)(_read_manifest)


def load_manifest() -> dict:
    """The parsed manifest; raises FileNotFoundError if the app hasn't been built.

    Re-read on every request while DEBUG is on, so a rebuild shows up without a restart.
    """
    path = manifest_path()
    return _read_manifest(path) if settings.DEBUG else _read_manifest_cached(path)


@register.simple_tag
def vite_assets(entry: str):
    manifest = load_manifest()

    # CSS belongs to the entry and to any chunks it imports.
    css: list[str] = []
    seen: set[str] = set()

    def collect_css(name: str) -> None:
        if name in seen:
            return
        seen.add(name)
        chunk = manifest[name]
        for imported in chunk.get("imports", []):
            collect_css(imported)
        css.extend(file for file in chunk.get("css", []) if file not in css)

    collect_css(entry)
    tags = [format_html('<link rel="stylesheet" href="{}">', static(file)) for file in css]
    tags.append(format_html('<script type="module" src="{}"></script>', static(manifest[entry]["file"])))
    return mark_safe("\n".join(tags))
