# budget_tracker

수입과 지출을 기록하고, 카테고리별 통계와 월간 리포트를 계산해주는 간단한 가계부 Python 패키지입니다.
대학교 1학년 Python 프로그래밍 기말 프로젝트로 제작했습니다.

> **GitHub 저장소**: (여기에 본인의 GitHub 저장소 URL을 적어주세요. 예: https://github.com/아이디/budget_tracker)

## 1. 프로젝트 개요

`budget_tracker`는 거래(Transaction)를 부모 클래스로 두고, 수입(Income)과 지출(Expense)을
자식 클래스로 상속받아 구현한 패키지입니다. `BudgetTracker` 클래스로 여러 거래를 모아
총 잔액, 카테고리별 통계, 월간 리포트를 계산할 수 있습니다.

- `Transaction` : 모든 거래의 공통 속성(금액, 카테고리, 설명, 날짜)을 가진 부모 클래스
- `Income` / `Expense` : `Transaction`을 상속하며 잔액에 +/- 로 반영되는 자식 클래스
- `BudgetTracker` : 여러 거래를 모아 통계를 계산하는 관리 클래스

## 2. 설치 방법

```bash
# 1) 가상환경 생성 및 활성화 (권장)
python -m venv .venv
source .venv/bin/activate     # Windows는 .venv\Scripts\activate

# 2) 패키지 설치
pip install .
```

## 3. 빠른 시작 (Quick Start)

```python
from budget_tracker import BudgetTracker, Income, Expense

tracker = BudgetTracker()
tracker.add_transaction(Income(500000, "월급", source="회사"))
tracker.add_transaction(Expense(30000, "식비", is_essential=True))
tracker.add_transaction(Expense(15000, "교통"))

print(tracker.total_balance())      # 455000.0
print(tracker.category_stats())     # {'월급': 500000.0, '식비': -30000.0, '교통': -15000.0}
print(tracker.monthly_report(2026, 6))
```

## 4. 주요 기능

| 기능 | 설명 |
|---|---|
| `Transaction` | 거래 1건의 금액·카테고리·설명·날짜를 검증하고 저장 |
| `Income.signed_amount()` | 수입은 잔액에 양수(+)로 반영 |
| `Expense.signed_amount()` | 지출은 잔액에 음수(-)로 반영 |
| `BudgetTracker.add_transaction()` | 거래 추가 (Transaction이 아니면 에러) |
| `BudgetTracker.total_balance()` | 전체 잔액(수입-지출) 계산 |
| `BudgetTracker.category_stats()` | 카테고리별 합계 계산 |
| `BudgetTracker.monthly_report(year, month)` | 특정 연/월의 수입·지출·순잔액 계산 |
| `BudgetTracker.save_to_csv(filepath)` | 모든 거래를 CSV 파일로 저장 |
| `BudgetTracker.load_from_csv(filepath)` | CSV 파일에서 거래 내역을 불러와 추가 |

## 5. 테스트 실행 방법

```bash
pip install pytest pycodestyle

# 단위 테스트 + docstring 안의 >>> 예시(doctest)까지 함께 실행
pytest tests/ --doctest-modules budget_tracker/ -v

# PEP 8 스타일 검사
pycodestyle budget_tracker/ tests/
```

## 6. 작성자 정보

- 이름 / 학번: 엄윤성 / 202620873
- 과목: Python 프로그래밍 (기말 프로젝트)
- 작성일: 2026년 6월
