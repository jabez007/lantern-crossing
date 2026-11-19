PYTHON ?= python3
PACKWIZ ?= packwiz
RUFF ?= ruff
PACK_CHANNEL ?= development
export PACK_CHANNEL
MRPACK = dist/$(shell $(PYTHON) scripts/release_metadata.py --field archive)

.NOTPARALLEL:
.PHONY: test lint validate refresh export checksum release clean

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

checksum: export
	$(PYTHON) scripts/release_metadata.py --checksum

# An explicit tag and owner-recorded runtime acceptance are required for release.
release: override PACK_CHANNEL = release
release: test lint checksum

clean:
	rm -rf build dist
