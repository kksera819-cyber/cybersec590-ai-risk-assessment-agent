# Testing Report — Assignment 2

## Test strategy
We use three levels of evidence: (1) deterministic policy/tool unit tests, (2) deterministic **mock LLM + simulated tool** end-to-end orchestration scenarios, and (3) a separate **live Duke AI Gateway baseline**. Mocked scenarios exercise the orchestration pipeline but do not demonstrate live model generalization. The expected outputs below are policy-derived and were specified before comparing the observed outcomes.

## Unit tests
User-observed terminal result: **11/11 passed** using `python -m unittest discover -s tests -v`. The test suite covers policy transitions, environment lookup, invalid tool request, missing evidence, external failure and rejection of unusable HTML. Preserve `outputs/unit_test_results_final.txt` as the execution log.

## End-to-end mocked orchestration tests
Source: `outputs/e2e_tests/report.md` and the user's terminal output. **6/6 passed**.

| Scenario | Controlled condition | Expected | Actual | Result |
|---|---|---|---|---|
| T1_confirmed | Confirmed applicability, high impact | High | High | PASS |
| T1_not_applicable | Non-applicability with high impact held constant | Low | Low | PASS |
| T2_high_impact | Confirmed applicability and high impact | High | High | PASS |
| T2_low_impact | Confirmed applicability and low impact | Medium | Medium | PASS |
| T3_missing_evidence | Missing decisive prerequisite evidence | Insufficient Evidence | Insufficient Evidence | PASS |
| T4_external_failure | External reference tool returns failure | Insufficient Evidence | Insufficient Evidence | PASS |

The exact fixtures are saved under `outputs/e2e_tests/<scenario>/fixture.json`. Each scenario also saves `agent_assessment.json` and `agent_trace.json`. Review fixtures before asserting which individual prerequisites were altered.

## Live model baseline
The live Duke Gateway baseline (`gpt-6-luna`) returned `applicability=potential`, `impact=unknown`, `decision=Insufficient Evidence`, rule `P1`. Tool trace recorded `lookup_environment` and `lookup_external_reference`. Source S02/S03 and contextual S05 were used. This is **one observed run**, not a statistical accuracy evaluation. Files: `outputs/baseline/agent_assessment.json` and `outputs/baseline/agent_trace.json`.

## Human evidence review — required before final submission
| Check | Reviewer observation | Status |
|---|---|---|
| S03 actually supports FILE04 signing exception | [VERIFY AGAINST SOURCE] | Pending |
| S02 does not imply internal SMB is unreachable | [VERIFY] | Pending |
| S05 is contextual, not FILE04-specific | [VERIFY] | Pending |
| Microsoft reference is accurately paraphrased and dated | [VERIFY] | Pending |
| Missing evidence is explicit and action items are safe | [VERIFY] | Pending |
| T1–T4 traces match expected tool outputs and decisions | [VERIFY] | Pending |

**Reviewer name/date:** [COMPLETE]  **Review outcome:** [COMPLETE]  **Corrections made:** [COMPLETE]

## Limitations and follow-up
The dataset is simulated and reconstructed from a course document. No live host scanning, NTLM authentication telemetry, SMB negotiation capture, or share ACL inspection was performed. The six scenario evaluations used mocked LLM/tool responses. Future validation should test multiple genuine model runs and obtain authorized network/configuration evidence before assigning an operational risk rating.
