.PHONY: dev test build binary pkg-arch pkg-deb pkg-rpm clean

BUILDDIR := .pkgbuild

PYTHON ?= $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)
VERSION := $(shell $(PYTHON) -c "import sys; sys.path.insert(0, 'src'); import rewire; print(rewire.__version__)")

dev:
	$(PYTHON) -m venv .venv
	.venv/bin/pip install -e ".[dev]"

test: dev
	.venv/bin/pytest

build: test
	.venv/bin/python -m build

binary: test
	.venv/bin/pyinstaller --onefile --name rewire --paths src entry.py

pkg-arch: build
	rm -rf $(BUILDDIR)
	mkdir -p $(BUILDDIR)
	cp PKGBUILD dist/rewire-$(VERSION).tar.gz $(BUILDDIR)/
	cd $(BUILDDIR) && makepkg -f -C

pkg-deb: build
	PYTHON="$(PYTHON)" ./pkg-deb

pkg-rpm: build
	PYTHON="$(PYTHON)" ./pkg-rpm

clean:
	pkill -f "rewire" -x || true
	rm -rf $(BUILDDIR)
	git clean -fdX || true