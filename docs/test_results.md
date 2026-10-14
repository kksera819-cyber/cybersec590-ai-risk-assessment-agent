# Test Results – Assignment 2

## Overview

I tested the risk policy and the agent workflow to check whether the results match the expected behavior. The project uses a simulated environment, so these tests do not prove that a real SMB relay attack is possible.

| Test type | Result | Evidence |
|---|---|---|
| Unit tests | 11/11 passed | `outputs/baseline/unit_test_results.txt` |
| Mock end-to-end scenarios | 6/6 passed | `outputs/e2e_tests/report.md` |
| Live Duke AI Gateway baseline | One successful run | `outputs/baseline/agent_assessment.json` and `agent_trace.json` |

## Policy and Failure Checks

The following results come from the recorded unit tests and mock scenarios. The mock scenarios use controlled LLM and tool responses rather than six separate live Gateway calls.

| Check | Expected | Observed | Result |
|---|---|---|---|
| Applicability changes from confirmed to not applicable, with high impact | High to Low | High to Low | Pass |
| Impact changes from high to low, with confirmed applicability | High to Medium | High to Medium | Pass |
| Missing decisive evidence | Insufficient Evidence | Insufficient Evidence | Pass |
| External reference lookup fails | Insufficient Evidence | Insufficient Evidence | Pass |

The unit test suite also checks that a URL outside the allowed external reference is blocked. This is a tool boundary check, not a separate live-model evaluation.

## Live Baseline

The successful Duke AI Gateway run used `gpt-6-luna`. The model requested both `lookup_environment` and `lookup_external_reference`.

| Field | Observed value |
|---|---|
| Applicability | `potential` |
| Impact | `unknown` |
| Decision | `Insufficient Evidence` |
| Policy rule | `P1: decisive evidence missing` |

The result makes sense for this case. FILE04 does not require SMB signing, but internal SMB reachability, NTLM relay prerequisites, and FILE04-specific impact are still unknown.

## Human Review and Limitations

I completed an individual self-review of the environment evidence and the agent assessment. The review is recorded in [HUMAN_REVIEW.md](HUMAN_REVIEW.md).

The six end-to-end scenarios were mocked, and only one successful live Gateway baseline was recorded. No penetration testing or verification against a real FILE04 server was performed. The original inputs, traces, and test results were saved for later comparison.

For test setup and scenario details, see [TESTING.md](TESTING.md).
