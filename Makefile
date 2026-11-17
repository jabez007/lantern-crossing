PYTHON ?= python3
PACKWIZ ?= packwiz
RUFF ?= ruff
PACK_VERSION := $(shell $(PYTHON) scripts/release_metadata.py --field version)
MRPACK := dist/lantern-crossing-$(PACK_VERSION).mrpack

.NOTPARALLEL:
.PHONY: test lint validate refresh export release clean

test:
	$(PYTHON) -m unittest discover -s tests -v

lint:
	$(RUFF) check scripts tests
	$(RUFF) format --check scripts tests

validate:
	$(PYTHON) scripts/release_metadata.py
	$(PYTHON) scripts/check_pack.py

refresh:
	$(PACKWIZ) refresh

# Validate before packwiz's implicit refresh, so export cannot hide a stale index.
export: validate
	mkdir -p dist
	$(PACKWIZ) modrinth export -o $(MRPACK)
	$(PYTHON) scripts/normalize_mrpack.py $(MRPACK)
	$(PYTHON) scripts/validate_mrpack.py $(MRPACK)

release: test lint export
	$(PYTHON) scripts/release_metadata.py --checksum

clean:
	rm -rf build dist
