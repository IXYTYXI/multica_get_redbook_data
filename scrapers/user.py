"""Author profile + their notes.

Endpoints: ``/api/sns/web/v1/user/otherinfo`` (profile) and
``/api/sns/web/v1/user_posted`` (their notes; carries ``xsec_token`` per note).

Stage 2: implement against the signed/browser client.
"""
from typing import List

from models.data import NoteInfo, XhsUserInfo


class UserScraper:
    def __init__(self, client=None):
        self.client = client

    async def get_user(self, user_id: str, xsec_token: str = "", xsec_source: str = "pc_user") -> XhsUserInfo:
        raise NotImplementedError("Stage 2: implement XHS author profile")

    async def get_user_notes(self, user_id: str, max_count: int = 50, xsec_token: str = "") -> List[NoteInfo]:
        raise NotImplementedError("Stage 2: implement XHS author notes listing")
