# pymupdf-stubs

[![PyPI](https://img.shields.io/pypi/v/pymupdf-stubs.svg)](https://pypi.org/project/pymupdf-stubs/)
[![Changelog](https://img.shields.io/github/v/release/elohmeier/pymupdf-stubs?include_prereleases&label=changelog)](https://github.com/elohmeier/pymupdf-stubs/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/elohmeier/pymupdf-stubs/blob/master/LICENSE)

Type stubs for [PyMuPDF](https://github.com/pymupdf/PyMuPDF) (`pymupdf` / `fitz`), published as a PEP 561 stub-only package.

## Installation

```bash
pip install -U pymupdf-stubs
```

This package targets current PyMuPDF releases.

## Usage

No runtime code changes are required. Install stubs and run your type checker.

```python
import pymupdf
import fitz

doc = pymupdf.Document()
page = doc[0]
drawings = page.get_drawings()
```

## Type Checking

This repository validates stubs with:

```bash
uv run ty check
```

## Compatibility Notes

- `fitz` is supported as a compatibility re-export of `pymupdf`.
- Some highly dynamic APIs may still be typed as `Any` or broad dictionary shapes.
- If a PyMuPDF API is missing or incorrect, please open an issue.

## Contributing

Issues and PRs are welcome: <https://github.com/elohmeier/pymupdf-stubs/issues>
