"""budget_tracker.subclass
===========================

:class:`Transaction` 을 상속하는 :class:`Income`, :class:`Expense` 클래스를 정의한다.
"""

from budget_tracker.core import Transaction


class Income(Transaction):
    """수입을 나타내는 클래스. 잔액에 양수(+)로 반영된다.

    :ivar source: 수입의 출처 (예: "월급", "용돈")

    >>> i = Income(50000, "월급", source="회사")
    >>> i.signed_amount()
    50000.0
    """

    def __init__(self, amount, category, description="", date=None, source=""):
        """Income 객체를 생성한다.

        :param amount: 수입 금액 (양수)
        :param category: 수입 분류
        :param description: 설명
        :param date: 날짜 ("YYYY-MM-DD"), None이면 오늘 날짜
        :param source: 수입의 출처
        """
        super().__init__(amount, category, description, date)
        self.source = source

    def signed_amount(self):
        """수입은 잔액에 양수로 더해진다.

        :return: 거래 금액 그대로(+)
        """
        return self.amount

    def to_dict(self):
        """부모의 to_dict() 결과에 source 필드를 추가한다.

        :return: 부모 필드 + source가 포함된 dict
        """
        data = super().to_dict()
        data["source"] = self.source
        return data


class Expense(Transaction):
    """지출을 나타내는 클래스. 잔액에 음수(-)로 반영된다.

    :ivar is_essential: 필수 지출 여부 (식비, 교통비 등이면 True)

    >>> e = Expense(10000, "식비", is_essential=True)
    >>> e.signed_amount()
    -10000.0
    """

    def __init__(self, amount, category, description="", date=None,
                 is_essential=False):
        """Expense 객체를 생성한다.

        :param amount: 지출 금액 (양수)
        :param category: 지출 분류
        :param description: 설명
        :param date: 날짜 ("YYYY-MM-DD"), None이면 오늘 날짜
        :param is_essential: 필수 지출 여부 (기본값: False)
        """
        super().__init__(amount, category, description, date)
        self.is_essential = is_essential

    def signed_amount(self):
        """지출은 잔액에 음수로 반영된다.

        :return: 거래 금액에 음수를 취한 값
        """
        return -self.amount

    def to_dict(self):
        """부모의 to_dict() 결과에 is_essential 필드를 추가한다.

        :return: 부모 필드 + is_essential이 포함된 dict
        """
        data = super().to_dict()
        data["is_essential"] = self.is_essential
        return data
