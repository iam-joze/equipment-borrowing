#!/usr/bin/env bash
# Verifies the Clean Architecture dependency rule by listing forbidden imports.
# Empty sections mean the dependencies point inward.
cd "$(dirname "$0")/.." || exit 1

echo "== domain: imports of application/infrastructure/interface =="
grep -rnE "^(from|import) equipment_borrowing\.(application|infrastructure|interface)" --include="*.py" src/equipment_borrowing/domain

echo "== application: imports of infrastructure/interface =="
grep -rnE "^(from|import) equipment_borrowing\.(infrastructure|interface)" --include="*.py" src/equipment_borrowing/application

echo "== infrastructure: imports of interface =="
grep -rnE "^(from|import) equipment_borrowing\.interface" --include="*.py" src/equipment_borrowing/infrastructure

echo "(empty sections above mean all dependencies point inward)"