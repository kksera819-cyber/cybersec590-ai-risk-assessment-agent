# Design – SMB Relay Risk Assessment Agent

## 1. Scenario and Risk Question

This project uses a fictional company called Northbridge Services. I focus on FILE04, one of four Windows Server 2022 file servers in the W05 group.

FILE04 does not require SMB signing. This could create an opportunity for an SMB relay attack, but the setting alone does not prove that an attack would work.

**Risk question:** Does FILE04's nonmandatory SMB signing create a meaningful SMB relay risk in this environment?

**Case ID:** `SMB-SIGNING-FILE04`

## 2. Agent Design

The architecture diagram is in [architecture.mmd](architecture.mmd).

I separated the work between the LLM, Python code, tools, and human review:

- **LLM:** Reads the risk question, selects tools, and analyzes applicability and possible impact.
- **Python:** Runs the requested tools, checks the model's output, applies the risk policy, and saves results.
- **Tools:** Read the simulated environment data and retrieve an approved Microsoft Learn reference.
- **Human review:** Checks the evidence and whether the final decision makes sense.

The LLM does not directly assign the final risk rating. Python applies the fixed policy after the model provides applicability and impact values.

## 3. Workflow

1. Load `data/threat_input.json` and the Duke AI Gateway settings.
2. Send the risk question and tool definitions to the model using `tool_choice=auto`.
3. The model requests `lookup_environment` and `lookup_external_reference` when it needs evidence.
4. Python runs the tool calls and saves their arguments, results, and errors in `outputs/agent_trace.json`.
5. The model uses the returned information to assess applicability and impact separately.
6. Python checks the output, applies `rate(applicability, impact)`, and saves `outputs/agent_assessment.json`.
7. I review the evidence and the decision in `docs/HUMAN_REVIEW.md`.

## 4. Tools

| Tool | Input | Purpose | If It Fails |
|---|---|---|---|
| `lookup_environment` | Asset ID, such as `FILE04` | Get asset details and simulated evidence | Return `not_found` for an unknown asset |
| `lookup_external_reference` | Approved Microsoft Learn URL | Get technical information about SMB signing | Return a blocked or unavailable status |

The external lookup only accepts the approved Microsoft Learn URL. The agent should treat website content as evidence, not as instructions.

The environment information is simulated. The Microsoft reference explains SMB signing in general and does not prove that FILE04 is exploitable.

## 5. Evidence Used

| Evidence | Main Finding | What Is Still Unknown |
|---|---|---|
| S02 | No public SMB access; unlisted inter-zone traffic is denied | Internal SMB reachability |
| S03 | FILE04 does not require SMB signing; SMB1 is disabled on W05 | Whether relevant SMB sessions are unsigned |
| S05 | File service problems could interrupt work or expose information; RTO 24h, RPO 8h | FILE04-specific shares and business impact |
| Microsoft Learn | SMB signing helps protect against relay attacks | Whether an attack is possible on FILE04 |

The simulated environment snapshot is dated **September 23, 2026**. S02, S03, and S05 come from the provided `Windows_Enterprise_Environment.docx` (pages 2–3 and 6). The project uses a smaller JSON dataset reconstructed from that document.

## 6. Risk Policy

The policy uses two fields:

- **Applicability:** `confirmed`, `potential`, `not_applicable`, or `unknown`
- **Impact:** `high`, `medium`, `low`, or `unknown`

| Applicability | High Impact | Medium Impact | Low Impact |
|---|---|---|---|
| Confirmed | High | High | Medium |
| Potential | Medium | Medium | Low |
| Not applicable | Low | Low | Low |
| Unknown | Insufficient Evidence | Insufficient Evidence | Insufficient Evidence |

The rules also handle unknown impact:

- **P0:** If the threat is not applicable, the decision is Low, even if impact is unknown.
- **P1:** If decisive applicability or impact information is missing, the decision is Insufficient Evidence.
- **P2:** Otherwise, use the table above.

These are rules I defined for this assignment, not a universal cybersecurity rating system. The Python code also checks for unsupported claims. For example, it should not accept confirmed applicability without evidence of the required attack conditions.

## 7. Baseline Result

I ran the agent through the Duke AI Gateway using `gpt-6-luna`. The saved result was:

| Field | Result |
|---|---|
| Applicability | `potential` |
| Impact | `unknown` |
| Decision | `Insufficient Evidence` |
| Rule | `P1: decisive evidence missing` |

The result makes sense because FILE04 does not require SMB signing, but the available data does not confirm internal attack paths, NTLM relay prerequisites, or the sensitivity of its shared files.

The next step would be to check the effective SMB signing settings, internal SMB access, authentication requirements, and FILE04 share permissions.

## 8. Acceptance Criteria

I used the following checks to decide whether the agent worked as intended:

- The model requests tools and the calls appear in the saved trace.
- The agent uses both simulated environment evidence and an external technical reference.
- The assessment includes the asset, threat, applicability, impact, decision, policy rule, evidence, unknowns, and recommended action.
- Changing applicability or impact produces the expected result under the policy.
- Missing evidence and external tool failures do not produce unsupported risk ratings.
- Inputs, outputs, and test results are saved so they can be compared in Assignment 4.

See [TESTING.md](TESTING.md) for the test cases and results.

## 9. Limitations and Failure Handling

The agent can encounter missing data, incorrect tool arguments, or external lookup failures. The tools return error statuses, and the policy avoids assigning a definite rating when important evidence is missing.

The simulated environment does not include every network path, authentication setting, or file classification. Also, a successful Microsoft documentation lookup does not prove that FILE04 is vulnerable.

This is a risk assessment exercise, not a penetration test. **Insufficient Evidence** does not mean that FILE04 is safe; it means more information is needed.

## 10. Human Review and Individual Contribution

This is an individual project. I worked on the scenario, design, Python implementation, tool integration, risk policy, testing, and documentation.

I completed a self-review of S02, S03, S05, the external reference, and the final risk decision. The results are documented in [HUMAN_REVIEW.md](HUMAN_REVIEW.md). This was not an independent peer review.

**AI assistance disclosure:** I used AI assistance to help develop and debug code, plan tests, and improve documentation. I checked the saved outputs and evidence against the project files and remain responsible for the final submission.
