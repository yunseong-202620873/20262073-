"""budget_tracker.utils 모듈에 대한 단위 테스트."""

import pytest

from budget_tracker.utils import get_today_str, parse_date, format_currency


def test_get_today_str_format():
    """get_today_str()이 'YYYY-MM-DD' 형식 문자열을 반환하는지 확인."""
    today = get_today_str()
    assert len(today) == 10
    assert today[4] == "-" and today[7] == "-"


def test_parse_date_valid():
    """올바른 형식의 날짜 문자열은 그대로 반환되어야 한다."""
    assert parse_date("2026-06-18") == "2026-06-18"


def test_format_currency():
    """format_currency()가 천 단위 구분 기호와 '원'을 붙이는지 확인."""
    assert format_currency(12000) == "12,000원"


def test_parse_date_invalid_format():
    """형식이 틀린 날짜 문자열은 ValueError를 발생시켜야 한다."""
    with pytest.raises(ValueError):
        parse_date("2026/06/18")


def test_parse_date_none_input():
    """None을 입력하면 ValueError를 발생시켜야 한다(엣지 케이스)."""
    with pytest.raises(ValueError):
        parse_date(None)
