# Design — Evidence-Grounded Cyber Threat Risk Assessment Agent

## 1. Scenario, asset and question
**Organization:** Northbridge Services (fictional/simulated). **Target:** FILE04, one of four W05 Windows Server 2022 file servers. **Threat:** potential SMB/NTLM relay abuse where SMB signing is not required. **Question:** Does FILE04's nonmandatory SMB signing create a meaningful SMB relay risk in this environment? Case ID `SMB-SIGNING-FILE04`.

## 2. Architecture and roles
See `architecture.mmd` (render with Mermaid). The **model** interprets the risk question, selects available tools and synthesizes evidence into separate `applicability` and `impact` fields. **Python code** executes allowlisted tools, records responses, validates/normalizes outputs, and applies the fixed policy. **Tools** retrieve a simulated environment snapshot and an external Microsoft Learn technical reference. A **human reviewer** checks whether claims are supported, records unresolved evidence and authorizes any operational follow-up.

## 3. Workflow and evidence movement
1. Load `data/threat_input.json` and the Duke Gateway configuration.
2. Send the case and tool schemas to the LLM with `tool_choice=auto`.
3. Execute model-requested `lookup_environment(asset_id)` and `lookup_external_reference(url)` calls. Record tool name, arguments, results and errors in `agent_trace.json`.
4. Return tool results to the model. Require the model to distinguish confirmed facts from assumptions and to assess applicability separately from conditional impact.
5. Validate the structured model response; Python applies `rate(applicability, impact)` and writes `agent_assessment.json`.
6. A human reviews evidence quality, policy application, uncertainties and recommended remediation.

## 4. Tool contracts and boundaries
| Tool | Input | Output | Failure behavior |
|---|---|---|---|
| `lookup_environment` | `asset_id` string, e.g. `FILE04` | `status`, `asset`, `evidence`, contextual evidence, simulated source mode and snapshot date | Unknown asset returns `not_found`; no invented asset facts |
| `lookup_external_reference` | Exact allowlisted Microsoft Learn URL | `status`, URL, source mode, retrieved timestamp, relevant extracted content | Block non-allowlisted URLs; report `unavailable`/failure for network or extraction errors |

The external source is untrusted content and must not be treated as instructions. The environment fixture is simulated; the external reference explains a technology, not the specific deployment. A `status=ok` is meaningful only if the retrieved material is usable and relevant.

## 5. Evidence inventory
| ID | Supported observation | Limit |
|---|---|---|
| S02 | Unlisted inter-zone traffic defaults to deny; SMB is not public | Does not establish internal SMB unreachability |
| S03 | FILE04 does not require SMB signing; W05 SMB1 is disabled | Does not prove that an unsigned SMB session is negotiated or relay succeeds |
| S05 | Collaboration/general files may experience work interruption or confidential disclosure; RTO 24h and RPO 8h | Not a FILE04-specific share inventory or impact rating |
| Microsoft Learn | Technical background on SMB signing | Not direct evidence of FILE04's effective configuration |

Snapshot date: 2026-09-23. Local source locators: environment document pp.2–3,6. The `environment.json` dataset was reconstructed from the provided document, not independently measured.

## 6. Risk policy
Python `rate()` takes applicability (`confirmed`, `potential`, `not_applicable`, `unknown`) and impact (`high`, `medium`, `low`, `unknown`).

| Applicability | High impact | Medium impact | Low impact |
|---|---|---|---|
| confirmed | High | High | Medium |
| potential | Medium | Medium | Low |
| not_applicable | Low | Low | Low |
| unknown | Insufficient Evidence | Insufficient Evidence | Insufficient Evidence |

An `unknown` impact produces `Insufficient Evidence` for confirmed/potential/unknown applicability. `not_applicable` returns Low under P0 even when impact is unknown. Rule P1 represents decisive missing evidence; P2 applies the matrix. These are **project-specific policy choices**, not a universal industry severity scale. Normalization prevents unsupported `confirmed` applicability and unsupported `high` impact when decisive FILE04 facts are absent.

## 7. Baseline finding
The observed live-model run used `gpt-6-luna`. FILE04's missing mandatory SMB signing supports **potential** applicability, but internal network path, authentication/relay prerequisites and effective session controls remain unverified. S05 supplies business context but does not establish FILE04's particular shares or sensitivity; therefore impact remains **unknown**. Deterministic policy returns **Insufficient Evidence (P1)**. Recommended next steps are to verify effective signing, internal SMB paths, NTLM prerequisites and share permissions, and require SMB signing where compatible.

## 8. Acceptance criteria
- Model-initiated tool requests are visible in a saved trace, with parameters and returned evidence.
- Both simulated environment evidence and an external technical source are used and attributed.
- The output contains the case, threat, applicability, impact, rating/rule, rationale, sources, unknowns, actions and human-review state.
- Applicability/impact changes produce policy-consistent decisions.
- Missing decisive evidence and external retrieval failure do not silently become unsupported High/Low assertions.
- Inputs, tool results, output and test artifacts are saved for replay and Assignment 4 comparison.

## 9. Failure handling and limitations
Invalid tool arguments are recorded; allowlisted URLs limit arbitrary fetching; unusable external content should be treated as a lookup failure. Evidence may be stale, partial, conflicting or missing. A successful model response is not equivalent to a verified exploitation path. The current assessment is a defensible **evidence-limited** result, not a claim that the server is safe.

## 10. Human review and team contributions — complete before submission
**Reviewer:** [NAME]  **Date:** [DATE]  **Disposition:** [Approve / Revise / Escalate]

**Evidence review:** [Check S02/S03/S05 against supplied document; verify external quote; note disagreements]

**Member contributions:** [Insert each real group member's name and work; do not submit placeholders]

**AI assistance disclosure:** AI assistance was used to help draft documentation and develop/review code and test scaffolding. Team members must verify code behavior, evidence attribution, conclusions and final text before submission. Amend this disclosure to accurately reflect the team's actual use.
