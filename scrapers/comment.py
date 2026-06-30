"""Comments.

Endpoints: ``/api/sns/web/v2/comment/page`` (first-level, cursor paging) and
``/api/sns/web/v2/comment/sub/page`` (sub-comments). Requires ``note_id`` +
``xsec_token``.

Stage 2: implement against the signed/browser client.
"""
from typing import List

from models.data import CommentInfo


class CommentScraper:
    def __init__(self, client=None):
        self.client = client

    async def get_comments(self, note_id: str, xsec_token: str, max_count: int = 100) -> List[CommentInfo]:
        raise NotImplementedError("Stage 2: implement XHS comments with cursor paging")
