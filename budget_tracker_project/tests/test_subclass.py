"""budget_tracker.subclass 모듈(Income, Expense)에 대한 단위 테스트."""

from budget_tracker.subclass import Income, Expense


def test_income_signed_amount_positive():
    """Income의 signed_amount()는 양수를 반환해야 한다."""
    income = Income(50000, "월급")
    assert income.signed_amount() == 50000.0


def test_expense_signed_amount_negative():
    """Expense의 signed_amount()는 음수를 반환해야 한다."""
    expense = Expense(15000, "쇼핑")
    assert expense.signed_amount() == -15000.0


def test_income_to_dict_includes_source():
    """Income.to_dict()에 source 필드가 포함되어야 한다(super() 활용 확인)."""
    income = Income(30000, "용돈", source="부모님")
    data = income.to_dict()
    assert data["source"] == "부모님"
    assert data["amount"] == 30000.0  # 부모 클래스 필드도 그대로 유지


def test_expense_to_dict_includes_is_essential():
    """Expense.to_dict()에 is_essential 필드가 포함되어야 한다(super() 활용 확인)."""
    expense = Expense(8000, "식비", is_essential=True)
    data = expense.to_dict()
    assert data["is_essential"] is True
    assert data["category"] == "식비"


def test_expense_default_is_essential_false():
    """is_essential을 지정하지 않으면 기본값 False여야 한다."""
    expense = Expense(2000, "기타")
    assert expense.is_essential is False
