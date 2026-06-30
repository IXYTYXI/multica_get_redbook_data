"""Note keyword search.

Endpoint: ``/api/sns/web/v1/search/notes``
Each result carries a per-note ``xsec_token`` (+ infer ``xsec_source=pc_search``)
that MUST be captured and threaded into note-detail and comment requests.

Stage 2: implement against the signed/browser client.
"""
from typing import List

from models.data import NoteInfo


class KeywordScraper:
    def __init__(self, client=None):
        self.client = client

    async def search_notes(self, keyword: str, max_count: int = 50) -> List[NoteInfo]:
        raise NotImplementedError("Stage 2: implement XHS note search + xsec_token extraction")
