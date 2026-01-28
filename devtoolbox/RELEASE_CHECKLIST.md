# Release Checklist (v1.0.0)

- [ ] Verify tests pass: `pytest`
- [ ] Lint clean: `ruff check .`
- [ ] Update version in `devtoolbox/__init__.py`
- [ ] Update version in `pyproject.toml`
- [ ] Confirm README examples still match CLI output
- [ ] Add demo GIF or screenshot to README
- [ ] Create release notes (`RELEASE_NOTES_v1.0.0.md`)
- [ ] Tag release: `git tag v1.0.0`
- [ ] Push tag to GitHub
- [ ] Create GitHub Release with notes
