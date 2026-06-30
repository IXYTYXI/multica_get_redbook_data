"""Xiaohongshu request signing (``x-s`` / ``x-t`` / ``x-s-common``).

INDEPENDENT IMPLEMENTATION — do not copy third-party (e.g. MediaCrawler fork)
source. That project is a validated reference for the *approach* only.

Approach (to be implemented in Stage 1, login-gated):
  Xiaohongshu requires a signature header set on virtually every web API call.
  The hard, obfuscated core value is computed by the *page's own* JavaScript
  inside a logged-in Playwright context (browser injection), and the surrounding
  header envelope (the ``x-s`` payload, the ``x-t`` millisecond timestamp, and
  ``x-s-common``) is assembled in Python from that core value plus cookie/device
  fields. This avoids reversing the obfuscated algorithm and is resilient to
  most of its updates.

Until Stage 1 lands, ``sign_request`` raises NotImplementedError so the scaffold
imports cleanly and the offline smoke test passes.
"""
from typing import Any, Dict, Optional, Union


async def sign_request(
    page: Any,
    uri: str,
    data: Optional[Union[Dict, str]] = None,
    method: str = "POST",
    a1: str = "",
) -> Dict[str, str]:
    """Return the signed header set for one request.

    Args:
        page: a logged-in Playwright page (Xiaohongshu open) used to compute the
            core signature value in-browser.
        uri: API path, e.g. ``/api/sns/web/v1/search/notes``.
        data: GET params or POST payload.
        method: ``GET`` or ``POST``.
        a1: the ``a1`` value from the login cookie (device fingerprint).

    Returns:
        ``{"x-s": ..., "x-t": ..., "x-s-common": ..., "x-b3-traceid": ...}``
    """
    raise NotImplementedError(
        "Stage 1: implement browser-injection signing against a logged-in session"
    )
