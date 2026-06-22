"""budget_tracker.core 모듈에 대한 단위 테스트."""

import pytest

from budget_tracker.core import Transaction, BudgetTracker
from budget_tracker.subclass import Income, Expense


# ---------- Transaction 관련 테스트 (정상 케이스) ----------

def test_transaction_valid_creation():
    """정상적인 금액과 카테고리로 Transaction이 생성되는지 확인."""
    t = Transaction(10000, "식비", "점심값", "2026-06-18")
    assert t.amount == 10000.0
    assert t.category == "식비"
    assert t.date == "2026-06-18"


def test_transaction_default_date():
    """date를 지정하지 않으면 오늘 날짜가 자동으로 채워지는지 확인."""
    t = Transaction(5000, "기타")
    assert len(t.date) == 10  # "YYYY-MM-DD" 형식 길이
    assert t.date.count("-") == 2


def test_transaction_to_dict():
    """to_dict()가 올바른 키와 값을 포함하는지 확인."""
    t = Transaction(3000, "교통", "버스비", "2026-06-01")
    d = t.to_dict()
    assert d["amount"] == 3000.0
    assert d["category"] == "교통"
    assert d["date"] == "2026-06-01"


def test_transaction_signed_amount_default_positive():
    """부모 클래스의 signed_amount()는 기본적으로 양수를 반환."""
    t = Transaction(1000, "기타")
    assert t.signed_amount() == 1000.0


# ---------- Transaction 관련 테스트 (엣지 케이스) ----------

def test_transaction_invalid_amount_negative():
    """금액이 음수면 ValueError가 발생해야 한다."""
    with pytest.raises(ValueError):
        Transaction(-500, "식비")


def test_transaction_invalid_amount_zero():
    """금액이 0이면 ValueError가 발생해야 한다."""
    with pytest.raises(ValueError):
        Transaction(0, "식비")


def test_transaction_invalid_amount_non_numeric():
    """금액이 숫자로 변환할 수 없는 값이면 ValueError가 발생해야 한다."""
    with pytest.raises(ValueError):
        Transaction("천원", "식비")


def test_transaction_invalid_empty_category():
    """category가 빈 문자열이면 ValueError가 발생해야 한다."""
    with pytest.raises(ValueError):
        Transaction(1000, "   ")


# ---------- BudgetTracker 관련 테스트 (정상 케이스) ----------

def test_budget_tracker_add_and_total_balance():
    """Income과 Expense를 추가했을 때 총 잔액이 올바르게 계산되는지 확인."""
    tracker = BudgetTracker()
    tracker.add_transaction(Income(50000, "월급"))
    tracker.add_transaction(Expense(20000, "식비"))
    assert tracker.total_balance() == 30000.0


def test_budget_tracker_category_stats():
    """카테고리별 합계가 올바르게 계산되는지 확인."""
    tracker = BudgetTracker()
    tracker.add_transaction(Expense(10000, "식비"))
    tracker.add_transaction(Expense(5000, "식비"))
    stats = tracker.category_stats()
    assert stats["식비"] == -15000.0


def test_budget_tracker_monthly_report():
    """특정 연/월의 수입, 지출, 순잔액이 올바르게 계산되는지 확인."""
    tracker = BudgetTracker()
    tracker.add_transaction(Income(100000, "월급", date="2026-06-01"))
    tracker.add_transaction(Expense(30000, "식비", date="2026-06-15"))
    tracker.add_transaction(Income(20000, "용돈", date="2026-05-20"))
    report = tracker.monthly_report(2026, 6)
    assert report["income"] == 100000.0
    assert report["expense"] == 30000.0
    assert report["net"] == 70000.0


# ---------- BudgetTracker 관련 테스트 (엣지 케이스) ----------

def test_budget_tracker_empty_total_balance():
    """거래가 하나도 없을 때 총 잔액은 0이어야 한다."""
    tracker = BudgetTracker()
    assert tracker.total_balance() == 0


def test_budget_tracker_add_invalid_type():
    """Transaction이 아닌 객체를 추가하면 TypeError가 발생해야 한다."""
    tracker = BudgetTracker()
    with pytest.raises(TypeError):
        tracker.add_transaction("이것은 거래가 아님")


# ---------- CSV 저장/불러오기 테스트 ----------

def test_save_and_load_csv_roundtrip(tmp_path):
    """save_to_csv()로 저장한 뒤 load_from_csv()로 불러오면 내용이 같아야 한다."""
    tracker = BudgetTracker()
    tracker.add_transaction(Income(50000, "월급", source="회사"))
    tracker.add_transaction(Expense(10000, "식비", is_essential=True))
    csv_path = tmp_path / "transactions.csv"

    tracker.save_to_csv(csv_path)

    loaded_tracker = BudgetTracker()
    loaded_tracker.load_from_csv(csv_path)

    assert len(loaded_tracker.transactions) == 2
    assert loaded_tracker.total_balance() == tracker.total_balance()


def test_load_from_csv_missing_file():
    """존재하지 않는 파일을 불러오면 FileNotFoundError가 발생해야 한다."""
    tracker = BudgetTracker()
    with pytest.raises(FileNotFoundError):
        tracker.load_from_csv("이런_파일은_없음.csv")
