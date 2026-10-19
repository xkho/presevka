.PHONY: build build-fast package banner specimen doctor install clean distclean

build:
	./scripts/build.sh

# Skip hinting for quick iteration on glyph variants; see README.
build-fast:
	PRESEVKA_HINT=none ./scripts/build.sh

package:
	./scripts/package.sh

# Redraw the README artwork from the fonts in dist/. Both renderers declare
# their own dependencies inline, and neither is part of the repository: they
# are artwork helpers, not build steps.
banner:
	uv run tools/render_banner.py

specimen:
	uv run tools/render_specimen.py

doctor:
	./scripts/doctor.sh

install:
	./scripts/install-user.sh

clean:
	./scripts/clean.sh

distclean: clean
	rm -rf .cache .venv
