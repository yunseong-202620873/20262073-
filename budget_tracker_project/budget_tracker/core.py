"""budget_tracker.core
======================

가계부의 핵심 로직을 담은 모듈.

이 모듈은 모든 거래의 기반이 되는 :class:`Transaction` 부모 클래스와,
여러 거래를 모아 통계를 계산하는 :class:`BudgetTracker` 클래스를 정의한다.
"""

import csv

from budget_tracker.utils import get_today_str, parse_date


class Transaction:
    """하나의 거래(수입 또는 지출)를 나타내는 부모 클래스.

    :class:`Income`, :class:`Expense` 가 이 클래스를 상속하여
    각자의 부호(+/-)와 추가 속성을 정의한다.

    :ivar amount: 거래 금액 (항상 0보다 큰 값)
    :ivar category: 거래 분류 (예: "식비", "월급")
    :ivar description: 거래에 대한 설명
    :ivar date: "YYYY-MM-DD" 형식의 날짜 문자열

    >>> t = Transaction(10000, "식비", "점심", "2026-06-18")
    >>> t.amount
    10000.0
    """

    def __init__(self, amount, category, description="", date=None):
        """Transaction 객체를 생성한다.

        :param amount: 거래 금액 (양수)
        :param category: 거래 분류 문자열
        :param description: 거래 설명 (기본값: 빈 문자열)
        :param date: "YYYY-MM-DD" 형식 날짜. None이면 오늘 날짜 사용
        :raises ValueError: amount가 0 이하이거나 숫자가 아닌 경우,
            또는 category가 빈 문자열인 경우
        """
        self.amount = self._validate_amount(amount)
        self.category = self._validate_category(category)
        self.description = description
        self.date = parse_date(date) if date else get_today_str()

    def _validate_amount(self, amount):
        """금액이 유효한 양수인지 검사하는 비공개 메서드.

        :param amount: 검사할 금액
        :return: float으로 변환된 금액
        :raises ValueError: 숫자가 아니거나 0 이하인 경우

        >>> Transaction(5000, "기타")._validate_amount(100)
        100.0
        """
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError(f"금액은 숫자여야 합니다: {amount!r}")
        if amount <= 0:
            raise ValueError(f"금액은 0보다 커야 합니다: {amount}")
        return amount

    def _validate_category(self, category):
        """카테고리 문자열이 비어 있지 않은지 검사하는 비공개 메서드.

        :param category: 검사할 카테고리 문자열
        :return: 공백이 제거된 카테고리 문자열
        :raises ValueError: 빈 문자열이거나 문자열이 아닌 경우
        """
        if not isinstance(category, str) or not category.strip():
            raise ValueError("category는 비어 있지 않은 문자열이어야 합니다.")
        return category.strip()

    def signed_amount(self):
        """이 거래가 잔액에 더해질 부호 있는 금액을 반환한다.

        부모 클래스에서는 기본적으로 양수를 반환하지만,
        :class:`Income`, :class:`Expense` 에서 각각의 부호로 재정의한다.

        :return: 부호가 적용된 금액
        """
        return self.amount

    def to_dict(self):
        """거래 정보를 딕셔너리로 변환한다.

        자식 클래스에서는 이 메서드를 호출(super)한 뒤
        자신만의 필드를 추가하여 DRY 원칙을 지킨다.

        :return: amount, category, description, date를 담은 dict

        >>> Transaction(1000, "기타", date="2026-01-01").to_dict()["amount"]
        1000.0
        """
        return {
            "type": self.__class__.__name__,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    def __str__(self):
        """사람이 읽기 좋은 문자열 표현을 반환한다.

        :return: "[날짜] 카테고리: 금액원 (설명)" 형식의 문자열
        """
        return (f"[{self.date}] {self.category}: "
                f"{self.amount:,.0f}원 ({self.description})")


class BudgetTracker:
    """여러 :class:`Transaction` 을 모아 관리하고 통계를 계산하는 클래스.

    :ivar transactions: 추가된 Transaction 객체들의 리스트
    """

    def __init__(self):
        """비어 있는 거래 목록으로 BudgetTracker를 생성한다."""
        self.transactions = []

    def add_transaction(self, transaction):
        """거래를 목록에 추가한다.

        :param transaction: 추가할 Transaction (또는 그 자식 클래스) 객체
        :raises TypeError: transaction이 Transaction의 인스턴스가 아닌 경우

        >>> tracker = BudgetTracker()
        >>> from budget_tracker.subclass import Income
        >>> tracker.add_transaction(Income(50000, "월급"))
        >>> len(tracker.transactions)
        1
        """
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction은 Transaction의 인스턴스여야 합니다.")
        self.transactions.append(transaction)

    def total_balance(self):
        """현재까지의 총 잔액(수입 - 지출)을 계산한다.

        :return: 모든 거래의 signed_amount() 합계. 거래가 없으면 0
        """
        return sum(t.signed_amount() for t in self.transactions)

    def category_stats(self):
        """카테고리별 금액 합계를 계산한다.

        :return: {카테고리: 합계} 형태의 딕셔너리. 거래가 없으면 빈 dict
        """
        stats = {}
        for t in self.transactions:
            stats[t.category] = stats.get(t.category, 0) + t.signed_amount()
        return stats

    def monthly_report(self, year, month):
        """특정 연/월의 수입, 지출, 순잔액을 계산한다.

        :param year: 조회할 연도 (예: 2026)
        :param month: 조회할 월 (1~12)
        :return: {"income": 총수입, "expense": 총지출, "net": 순잔액} dict
        """
        monthly = self._filter_by_month(year, month)
        income = sum(
            t.signed_amount() for t in monthly if t.signed_amount() > 0
        )
        expense = sum(
            -t.signed_amount() for t in monthly if t.signed_amount() < 0
        )
        return {"income": income, "expense": expense, "net": income - expense}

    def _filter_by_month(self, year, month):
        """특정 연/월에 해당하는 거래만 골라내는 비공개 메서드.

        :param year: 연도
        :param month: 월
        :return: 해당 연/월의 Transaction 리스트
        """
        prefix = f"{year:04d}-{month:02d}"
        return [t for t in self.transactions if t.date.startswith(prefix)]

    def save_to_csv(self, filepath):
        """현재까지의 모든 거래를 CSV 파일로 저장한다.

        각 거래의 ``to_dict()`` 결과를 한 행(row)으로 저장하며,
        Income/Expense 어느 쪽에서 와도 같은 형식으로 기록된다.

        :param filepath: 저장할 CSV 파일 경로

        >>> tracker = BudgetTracker()
        >>> from budget_tracker.subclass import Income
        >>> tracker.add_transaction(Income(1000, "용돈"))
        >>> tracker.save_to_csv("_doctest_tmp.csv")
        >>> import os
        >>> os.path.exists("_doctest_tmp.csv")
        True
        >>> os.remove("_doctest_tmp.csv")
        """
        fieldnames = ["type", "amount", "category", "description",
                      "date", "source", "is_essential"]
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, restval="")
            writer.writeheader()
            for transaction in self.transactions:
                writer.writerow(transaction.to_dict())

    def load_from_csv(self, filepath):
        """CSV 파일에서 거래 내역을 읽어와 현재 목록에 추가한다.

        ``save_to_csv()`` 로 저장한 파일을 다시 불러올 때 사용한다.
        파일의 "type" 열 값(Income/Expense)에 따라 알맞은 클래스로
        객체를 복원한다.

        :param filepath: 읽어올 CSV 파일 경로
        :raises FileNotFoundError: 파일이 존재하지 않는 경우
        """
        # 순환 import(circular import)를 피하기 위해 메서드 안에서 import.
        from budget_tracker.subclass import Income, Expense

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                amount = float(row["amount"])
                category = row["category"]
                description = row["description"]
                date = row["date"]
                if row["type"] == "Income":
                    transaction = Income(
                        amount, category, description, date,
                        source=row.get("source", ""),
                    )
                elif row["type"] == "Expense":
                    transaction = Expense(
                        amount, category, description, date,
                        is_essential=(row.get("is_essential") == "True"),
                    )
                else:
                    continue
                self.transactions.append(transaction)
