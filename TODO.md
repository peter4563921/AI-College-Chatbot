# TODO

- [ ] Inspect all Python files for MySQL usage and identify the exact connection path for `/chat`.
- [x] Fix `backend/db.py` to ensure MySQL pool is initialized with correct credentials and does not persist bad auth configuration.

- [ ] Add targeted logging around pool creation/auth failure.
- [ ] Run a quick local test: `/health` and `/chat` POST to confirm the 1045 error is resolved.

