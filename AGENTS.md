# Agent Notes

## Testing Procedure

- Run stub/type checks with `uv run ty check`.
- This is the primary validation command for stub changes in this repository.

## Local PyMuPDF Source

- Use the local PyMuPDF checkout for API/signature reference:
  - `$HOME/repos/github.com/pymupdf/PyMuPDF`
- Prefer checking upstream definitions there (for example `src/__init__.py`) before updating stubs.
