"""Note detail.

Endpoint: ``/api/sns/web/v1/feed`` (POST), requires ``note_id`` + ``xsec_token``
(+ ``xsec_source``). A bare note_id cannot be resolved (risk-control 300017).

Stage 2: implement against the signed/browser client.
"""
from models.data import NoteInfo


class NoteScraper:
    def __init__(self, client=None):
        self.client = client

    async def get_note(self, note_id: str, xsec_token: str, xsec_source: str = "pc_search") -> NoteInfo:
        raise NotImplementedError("Stage 2: implement XHS note detail with token passthrough")
