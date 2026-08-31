.PHONY: dev test build binary pkg-arch clean

BUILDDIR := .pkgbuild

dev:
	python -m venv .venv
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
	cp PKGBUILD dist/rewire-0.1.1.tar.gz $(BUILDDIR)/
	cd $(BUILDDIR) && makepkg -f -C

clean:
	pkill -f "rewire" -x || true
	rm -rf $(BUILDDIR)
	git clean -fdX || true