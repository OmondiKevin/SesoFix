# SesoFix local commands: data preparation and engineering checks only.

VENV_PYTHON := .venv/bin/python
PYTHON ?= $(if $(wildcard $(VENV_PYTHON)),$(VENV_PYTHON),python3)

.PHONY: help test profile train train-custom

help:
	@echo "make test     Run engineering tests"
	@echo "make profile  Profile the local Common Voice 26.0 release"
	@echo "Model training is disabled locally and will run only in Google Colab."

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

profile:
	$(PYTHON) scripts/profile_common_voice_refresh.py

train train-custom:
	@echo "ERROR: SesoFix model training is Colab-only by project policy."
	@false
