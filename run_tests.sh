#!/bin/bash

poetry run pytest --cov=tbsky_booking -n 6 --cov-report=term-missing:skip-covered --cov-fail-under=80 tests/