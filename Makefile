.PHONY: build build-fast package banner specimen doctor install clean distclean

build:
	./scripts/build.sh

# Skip hinting for quick iteration on glyph variants; see README.
build-fast:
	PRESEVKA_HINT=none ./scripts/build.sh

package:
	./scripts/package.sh

# Redraw the README banners from the fonts in dist/. Declares its own
# dependencies inline, so it needs no entry in pyproject.toml.
banner:
	uv run tools/render_banner.py

# Redraw the README weight-axis specimen from the fonts in dist/.
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
