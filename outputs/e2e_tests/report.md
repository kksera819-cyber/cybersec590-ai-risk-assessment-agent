# End-to-End Agent Orchestration Tests

Mode: deterministic mocked LLM and simulated tools; these are NOT live Duke Gateway evaluations.

| Scenario | Expected | Actual | Result |
|---|---|---|---|
| T1_confirmed | High | High | PASS |
| T1_not_applicable | Low | Low | PASS |
| T2_high_impact | High | High | PASS |
| T2_low_impact | Medium | Medium | PASS |
| T3_missing_evidence | Insufficient Evidence | Insufficient Evidence | PASS |
| T4_external_failure | Insufficient Evidence | Insufficient Evidence | PASS |

Each scenario directory contains fixture.json, agent_assessment.json, and agent_trace.json.
The live Duke Gateway baseline remains in outputs/baseline/.
