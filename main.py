#!/usr/bin/env python3
"""xhs-scraper CLI entry point.

Currently only the offline `check` smoke test is wired; search/user/note/comment
land in Stage 2 (login-gated).
"""
import argparse
import sys


def cmd_check() -> int:
    """Offline smoke test: build models, exercise date filter, import modules."""
    from models.data import NoteInfo, XhsUserInfo, CommentInfo
    from core.datefilter import date_bounds, in_date_range
    from storage.feishu import (
        note_to_feishu_record,
        user_to_feishu_record,
        comment_to_feishu_record,
    )
    from storage.downloader import download_note_media
    import core.sign  # noqa: F401  (import-only; signing lands in Stage 1)
    import core.browser  # noqa: F401
    from scrapers.keyword import KeywordScraper  # noqa: F401
    from scrapers.note import NoteScraper  # noqa: F401
    from scrapers.comment import CommentScraper  # noqa: F401
    from scrapers.user import UserScraper  # noqa: F401

    note = NoteInfo(note_id="n1", title="t", author_nickname="a", image_urls="")
    user = XhsUserInfo(user_id="u1", nickname="a")
    comment = CommentInfo(comment_id="c1", note_id="n1", content="hi")

    # record converters
    assert note_to_feishu_record(note)["标题"] == "t"
    assert user_to_feishu_record(user)["用户ID"] == "u1"
    assert comment_to_feishu_record(comment)["评论ID"] == "c1"

    # date filter
    s, e = date_bounds("2025-01-01", "2025-06-01")
    assert s is not None and e is not None and s < e
    assert in_date_range(None, None, None) is True

    # downloader no-op on empty media
    assert download_note_media(note)["cover"] is None

    print("xhs-scraper scaffold OK")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="xhs-scraper")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("check", help="offline smoke test (no network/login)")
    args = parser.parse_args()

    if args.command == "check":
        return cmd_check()
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
