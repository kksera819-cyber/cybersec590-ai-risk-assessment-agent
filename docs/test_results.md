# Predeclared policy checks

| Test | Expected | Actual |
|---|---|---|
| Applicability confirmed/high impact -> not applicable/high impact | High -> Low | Run tests to verify |
| Impact high -> low with confirmed applicability | High -> Medium | Run tests to verify |
| Missing decisive applicability fact | Insufficient Evidence | Run tests to verify |
| Invalid external tool URL | blocked, no invented evidence | Run tests to verify |

These are unit checks, not a full end-to-end agent evaluation. Human review and full-run evidence remain pending.
