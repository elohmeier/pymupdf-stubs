# Agent Notes

## Testing Procedure

- Run stub/type checks with `uv run ty check`.
- This is the primary validation command for stub changes in this repository.

## Local PyMuPDF Source

- Use the local PyMuPDF checkout for API/signature reference:
  - `$HOME/repos/github.com/pymupdf/PyMuPDF`
- Prefer checking upstream definitions there (for example `src/__init__.py`) before updating stubs.

## Releasing

- Releases are automated by `.github/workflows/publish.yml`.
- Pushes to `main` that change package-relevant files run `uv run ty check`, compute the next release version, create the GitHub release, build, and publish.
- A weekly scheduled run checks PyPI for a newer `pymupdf` release, updates the stub package version/dependency/lockfile, validates with `uv run ty check`, then releases and publishes if validation passes.
