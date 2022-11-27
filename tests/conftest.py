from __future__ import annotations

from hypothesis import settings

settings.register_profile("ci", deadline=None)
settings.load_profile("ci")
