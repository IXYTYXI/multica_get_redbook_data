"""Playwright browser manager for Xiaohongshu.

Holds a logged-in browser context (seeded from the ``XHS_COOKIE`` cookie string)
and exposes an in-page ``fetch`` so signed requests inherit the page's runtime
state. Playwright is imported lazily so the offline smoke test does not require
the browser to be installed.

Stage 1 wires this together with ``core.sign.sign_request``.
"""
import asyncio
from typing import Optional

from config.settings import XHS_BASE_URL, XHS_COOKIE, PROXY_URL


def _cookie_string_to_list(cookie_str: str, domain: str = ".xiaohongshu.com") -> list:
    cookies = []
    for item in cookie_str.split(";"):
        item = item.strip()
        if "=" in item:
            name, value = item.split("=", 1)
            cookies.append(
                {"name": name.strip(), "value": value.strip(), "domain": domain, "path": "/"}
            )
    return cookies


class XhsBrowser:
    def __init__(self, cookie: str = ""):
        self._cookie = cookie or XHS_COOKIE
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    async def start(self, headless: bool = True):
        from playwright.async_api import async_playwright  # lazy

        self._playwright = await async_playwright().start()
        launch_args = {"headless": headless, "args": ["--no-sandbox", "--disable-gpu"]}
        if PROXY_URL:
            launch_args["proxy"] = {"server": PROXY_URL}
        self._browser = await self._playwright.chromium.launch(**launch_args)
        self._context = await self._browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        if self._cookie:
            await self._context.add_cookies(_cookie_string_to_list(self._cookie))
        self._page = await self._context.new_page()

    async def navigate(self, url: str):
        try:
            await self._page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception:
            pass
        await asyncio.sleep(2)

    async def cookie_dict(self) -> dict:
        cookies = await self._context.cookies()
        return {c["name"]: c["value"] for c in cookies}

    async def fetch_api(self, url: str, headers: Optional[dict] = None, method: str = "GET", body: Optional[dict] = None) -> dict:
        """Run fetch inside the page so credentials/runtime state are inherited."""
        try:
            return await self._page.evaluate(
                """async ({url, headers, method, body}) => {
                    const opts = {method, headers: {'Accept': 'application/json', ...headers}, credentials: 'include'};
                    if (body) { opts.body = JSON.stringify(body); opts.headers['Content-Type'] = 'application/json;charset=UTF-8'; }
                    const resp = await fetch(url, opts);
                    return await resp.json();
                }""",
                {"url": url, "headers": headers or {}, "method": method, "body": body},
            )
        except Exception as e:
            print(f"[Browser fetch error] {e}")
            return {}

    @property
    def page(self):
        return self._page

    async def close(self):
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *args):
        await self.close()
