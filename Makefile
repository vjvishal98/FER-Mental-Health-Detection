PYTHON=python
PIP=$(PYTHON) -m pip

.PHONY: install-dev test smoke run

install-dev:
	$(PIP) install --upgrade pip; $(PIP) install -r requirements-dev.txt

test:
	$(PYTHON) -m pytest -q

smoke:
	$(PYTHON) full_smoke_test.py

run:
	$(PYTHON) -m streamlit run dashboard.py --server.port 8502
