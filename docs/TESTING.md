# Testing Report — Assignment 2

## 1. How I Tested the Agent

I used three types of tests to check my risk assessment agent:

1. **Unit tests:** Check the Python risk policy and tool behavior.
2. **Mock end-to-end (E2E) tests:** Check how the agent handles different scenarios using simulated model and tool responses.
3. **Live Duke AI Gateway run:** Check that the agent can call tools and produce an assessment with a real model.

I compared the expected results with the actual outputs. The expected decisions were based on the risk policy described in [DESIGN.md](DESIGN.md).

## 2. Unit Tests

I ran the following command from the project folder:

```powershell
python -m unittest discover -s tests -v
```

**Result: 11 out of 11 tests passed.**

These tests cover risk policy decisions, environment lookup, invalid tool requests, missing evidence, external lookup failures, and unusable external content.

The saved baseline test log is in `outputs/baseline/unit_test_results.txt`.

## 3. Mock End-to-End Tests

I also tested six scenarios with mocked LLM and tool responses. This let me change specific conditions and check whether the agent followed the policy without depending on live model responses.

**Result: 6 out of 6 scenarios passed.**

| Scenario | Test Condition | Expected | Actual | Result |
|---|---|---|---|---|
| T1_confirmed | Confirmed applicability, high impact | High | High | Pass |
| T1_not_applicable | Not applicable, high impact | Low | Low | Pass |
| T2_high_impact | Confirmed applicability, high impact | High | High | Pass |
| T2_low_impact | Confirmed applicability, low impact | Medium | Medium | Pass |
| T3_missing_evidence | Important evidence is missing | Insufficient Evidence | Insufficient Evidence | Pass |
| T4_external_failure | External lookup fails | Insufficient Evidence | Insufficient Evidence | Pass |

The T1 scenarios check how changing applicability affects the decision. The T2 scenarios check how changing impact affects the decision. T3 checks missing evidence, and T4 checks a controlled tool failure.

The scenario files are saved under `outputs/e2e_tests/`. Each scenario includes its input fixture, assessment, and trace. The overall results are saved in `outputs/e2e_tests/report.md` and `outputs/e2e_tests/report.json`.

**Important:** These six tests use mocked responses. They are not six separate live Duke AI Gateway runs.

## 4. Live Agent Run

I ran the agent using the Duke AI Gateway with the `gpt-6-luna` model.

The saved trace shows calls to both `lookup_environment` and `lookup_external_reference`. The agent used simulated environment evidence and a live Microsoft technical reference.

The final output was:

| Field | Result |
|---|---|
| Applicability | potential |
| Impact | unknown |
| Decision | Insufficient Evidence |
| Policy rule | P1: decisive evidence missing |

I think this result makes sense because FILE04 does not require SMB signing, but the available evidence does not confirm internal reachability, relay prerequisites, or the impact on FILE04's files.

The saved live run is available in:

- `outputs/baseline/agent_assessment.json`
- `outputs/baseline/agent_trace.json`

This is one successful live run, so it does not show how consistently the model would perform across many runs.

## 5. Human Evidence Review

I completed an individual self-review of the environment evidence and the agent's final assessment. I checked that S02, S03, and S05 matched the simulated dataset, that the Microsoft reference was used for technical background, and that the final decision followed the risk policy.

I did not find any major inconsistencies in the evidence or the baseline risk decision.

The full review, including the review date and limitations, is documented in [HUMAN_REVIEW.md](HUMAN_REVIEW.md). Since this is an individual project, this was a self-review rather than an independent peer review.

## 6. Limitations and Next Steps

The environment is simulated, and I did not scan FILE04 or perform a real SMB relay attack. I also did not collect live network traffic, authentication logs, or share permissions.

The mock E2E tests are useful for checking the program's logic, but they do not measure the accuracy of the live model. For future work, I would run more live tests and compare the results with additional verified environment evidence.

I kept the baseline inputs, outputs, and traces so they can be used again for Assignment 4.
