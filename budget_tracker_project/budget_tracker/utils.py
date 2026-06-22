"""budget_tracker.utils
========================

날짜 처리, 금액 포맷 등 여러 클래스에서 공통으로 쓰이는 도우미 함수 모음.
"""

from datetime import datetime


def get_today_str():
    """오늘 날짜를 "YYYY-MM-DD" 형식 문자열로 반환한다.

    :return: 오늘 날짜 문자열
    """
    return datetime.today().strftime("%Y-%m-%d")


def parse_date(date_str):
    """날짜 문자열이 "YYYY-MM-DD" 형식인지 검사하고 그대로 반환한다.

    :param date_str: 검사할 날짜 문자열
    :return: 형식이 올바른 경우 동일한 날짜 문자열
    :raises ValueError: 형식이 올바르지 않은 경우

    >>> parse_date("2026-06-18")
    '2026-06-18'
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError(f"날짜는 'YYYY-MM-DD' 형식이어야 합니다: {date_str!r}")
    return date_str


def format_currency(amount):
    """숫자를 "12,000원" 형식의 문자열로 변환한다.

    :param amount: 변환할 금액 (int 또는 float)
    :return: 천 단위 구분 기호가 포함된 금액 문자열

    >>> format_currency(12000)
    '12,000원'
    """
    return f"{amount:,.0f}원"
