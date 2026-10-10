# Equipment Borrowing: DDD, TDD and Clean Architecture

Small lab-equipment loan system for the Makerere DDD/TDD/Clean Architecture
group coursework. Two connected use cases (ApproveLoan and CheckOutEquipment),
connected by the `LoanApproved` domain event. In-memory persistence only.

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the tests

```
python -m pytest -v
```

## Run the demo

```
PYTHONPATH=src python -m equipment_borrowing.interface.main
```

## Check the dependency rule

```
bash scripts/check_dependencies.sh
```

## Layout

- `src/equipment_borrowing/domain`: entities, value object, aggregates, domain service, event, errors
- `src/equipment_borrowing/application`: application service, event handler, DTOs, repository and dispatcher interfaces
- `src/equipment_borrowing/infrastructure`: in-memory repositories, in-process dispatcher
- `src/equipment_borrowing/interface`: entry point and composition root
- `tests`: T1-T8
- `evidence`: test runs, TDD fail/pass output, dependency check, demo run

## AI usage

Claude (Anthropic) was used to help plan the design and guide the step-by-step
implementation. The group reviewed the code and can explain it.