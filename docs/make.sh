#!/usr/bin/env sh

SPHINX_APIDOC_OPTIONS='members' poetry run sphinx-apidoc -o docs/_build -M -T shinyutils
mv docs/_build/shinyutils.rst docs/_build/index.rst
poetry run sphinx-build -D highlight_language=python -b markdown -c docs -d docs/_build/.doctrees docs/_build docs
