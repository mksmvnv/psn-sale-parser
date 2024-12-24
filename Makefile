.PHONY: all run lint
.SILENT: all run lint

WORKDIR=src
POETRY=poetry run
BLACKFLAGS=--config pyproject.toml

all: lint run

run:
	$(POETRY) python3 $(WORKDIR)/main.py

lint:
	$(POETRY) black $(BLACKFLAGS) $(WORKDIR)