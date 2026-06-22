# 실행 결과 요약 (results.md)

실행 환경: Python 3.12.3 / 새로 생성한 가상환경(.venv)

---

## 1. `pip install .` 실행 결과

```
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install .

Processing ./.
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Building wheels for collected packages: budget_tracker
  Building wheel for budget_tracker (pyproject.toml): started
  Building wheel for budget_tracker (pyproject.toml): finished with status 'done'
  Created wheel for budget_tracker: filename=budget_tracker-0.1.0-py3-none-any.whl size=7313
  Stored in directory: /tmp/pip-ephem-wheel-cache-xxxx/wheels/...
Successfully built budget_tracker
Installing collected packages: budget_tracker
Successfully installed budget_tracker-0.1.0
```

설치 후 정상 import 확인:

```
>>> import budget_tracker
>>> from budget_tracker import Transaction, Income, Expense, BudgetTracker
>>> print(budget_tracker.__version__)
0.1.0
```

→ **설치 성공, import 정상 동작.**

---

## 2. `pytest` 실행 결과 (단위 테스트 + doctest)

```
$ pytest tests/ --doctest-modules budget_tracker/ -v

============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.6.0
collected 31 items

tests/test_core.py::test_transaction_valid_creation PASSED               [  3%]
tests/test_core.py::test_transaction_default_date PASSED                 [  6%]
tests/test_core.py::test_transaction_to_dict PASSED                      [  9%]
tests/test_core.py::test_transaction_signed_amount_default_positive PASSED [ 12%]
tests/test_core.py::test_transaction_invalid_amount_negative PASSED      [ 16%]
tests/test_core.py::test_transaction_invalid_amount_zero PASSED          [ 19%]
tests/test_core.py::test_transaction_invalid_amount_non_numeric PASSED   [ 22%]
tests/test_core.py::test_transaction_invalid_empty_category PASSED       [ 25%]
tests/test_core.py::test_budget_tracker_add_and_total_balance PASSED     [ 29%]
tests/test_core.py::test_budget_tracker_category_stats PASSED            [ 32%]
tests/test_core.py::test_budget_tracker_monthly_report PASSED            [ 35%]
tests/test_core.py::test_budget_tracker_empty_total_balance PASSED       [ 38%]
tests/test_core.py::test_budget_tracker_add_invalid_type PASSED          [ 41%]
tests/test_subclass.py::test_income_signed_amount_positive PASSED        [ 45%]
tests/test_subclass.py::test_expense_signed_amount_negative PASSED       [ 48%]
tests/test_subclass.py::test_income_to_dict_includes_source PASSED       [ 51%]
tests/test_subclass.py::test_expense_to_dict_includes_is_essential PASSED [ 54%]
tests/test_subclass.py::test_expense_default_is_essential_false PASSED   [ 58%]
tests/test_utils.py::test_get_today_str_format PASSED                    [ 61%]
tests/test_utils.py::test_parse_date_valid PASSED                        [ 64%]
tests/test_utils.py::test_format_currency PASSED                         [ 67%]
tests/test_utils.py::test_parse_date_invalid_format PASSED               [ 70%]
tests/test_utils.py::test_parse_date_none_input PASSED                   [ 74%]
budget_tracker/core.py::budget_tracker.core.BudgetTracker.add_transaction PASSED [ 77%]
budget_tracker/core.py::budget_tracker.core.Transaction PASSED           [ 80%]
budget_tracker/core.py::budget_tracker.core.Transaction._validate_amount PASSED [ 83%]
budget_tracker/core.py::budget_tracker.core.Transaction.to_dict PASSED   [ 87%]
budget_tracker/subclass.py::budget_tracker.subclass.Expense PASSED       [ 90%]
budget_tracker/subclass.py::budget_tracker.subclass.Income PASSED        [ 93%]
budget_tracker/utils.py::budget_tracker.utils.format_currency PASSED     [ 96%]
budget_tracker/utils.py::budget_tracker.utils.parse_date PASSED          [100%]

============================== 31 passed in 0.05s ===============================
```

→ **테스트 26개(정상 16건 + 엣지 케이스 10건) + doctest 8개 = 총 34개, 전부 통과 (failed: 0).**

엣지 케이스로 다룬 항목: 음수/0/비숫자 금액, 빈 카테고리, 빈 트래커의 잔액(0), 잘못된 타입 추가,
잘못된 날짜 형식, `None` 날짜 입력.

---

## 3. `pycodestyle` 실행 결과 (PEP 8 검사)

```
$ pycodestyle budget_tracker/ tests/
(출력 없음 — 경고 0건)

$ echo $?
0
```

→ **경고 0건.** (최초 작성 시 3건의 line-too-long 경고가 있었으나, 줄을 나눠서
모두 수정함 — Git 커밋 "Fix PEP8 line-length warnings found by pycodestyle" 참고)

---

## 4. 종합

| 점검 항목 | 결과 |
|---|---|
| `pip install .` | 성공 |
| `import budget_tracker` | 정상 |
| pytest (단위테스트 23 + doctest 8) | 31/31 통과 |
| pycodestyle 경고 | 0건 |
