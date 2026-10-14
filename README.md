# Assignment 2 — Evidence-Grounded SMB Relay Risk Agent

## Overview
This project evaluates a **simulated** Northbridge Services Windows Server 2022 file server, **FILE04**, for potential SMB/NTLM relay risk associated with nonmandatory SMB signing. The agent uses an LLM through the Duke AI Gateway to select and call tools, collects environment evidence and a Microsoft technical reference, and then applies a deterministic Python risk policy. This is a defensive assessment, **not** a penetration test or proof of exploitation.

**Case question:** Does FILE04's nonmandatory SMB signing create a meaningful SMB relay risk in this environment?

**Observed live-model baseline:** `applicability=potential`, `impact=unknown`, `decision=Insufficient Evidence` (`P1`). The missing facts include internal SMB reachability, relay prerequisites, and FILE04-specific share classification.

## Requirements and setup
- Python 3.10+ recommended; install dependencies using the requirements files provided with the existing project (including `openai` and `python-dotenv`).
- Create a local `.env` file (never commit it):

```dotenv
LITELLM_TOKEN=YOUR_DUKE_GATEWAY_TOKEN
DUKE_GATEWAY_URL=https://litellm.oit.duke.edu/v1
DUKE_MODEL=gpt-6-luna
```

- A valid Duke Gateway credential and network access are needed for the live run.

## Run
From the repository root:

```powershell
python -m src.agent
python -m unittest discover -s tests -v
python -m scripts.run_e2e_tests
```

The live agent writes `outputs/agent_assessment.json` and `outputs/agent_trace.json`. The deterministic E2E harness writes separate scenario artifacts under `outputs/e2e_tests/`. A preserved successful live baseline is under `outputs/baseline/`.

## Project structure
- `data/environment.json`: reconstructed simulated asset/evidence snapshot (not a live CMDB).
- `data/threat_input.json`: risk question and approved external reference.
- `src/tools.py`: environment lookup and allowlisted external reference lookup.
- `src/agent.py`: LLM orchestration, tool dispatch, output normalization and trace.
- `src/risk_policy.py`: deterministic rating policy.
- `tests/`: unit and mock-agent orchestration tests.
- `scripts/run_e2e_tests.py`: scenario runner.
- `docs/DESIGN.md`: workflow, contracts, policy, acceptance criteria and limitations.
- `docs/TESTING.md`: expected-versus-observed tests and evidence review checklist.
- `docs/architecture.mmd`: Mermaid architecture diagram.

## Evidence provenance
Environment facts are **simulated/reconstructed from the supplied Windows_Enterprise_Environment.docx** (snapshot 2026-09-23); source locators S02, S03 and S05 refer to that document. The Microsoft Learn page is an external live reference, not proof of FILE04's actual state. A successful HTTP retrieval alone is not sufficient to establish an evidentiary claim; relevant extracted content should be preserved in the trace.

## Security and limitations
- Do not commit `.env`, tokens, or any private logs containing credentials. Use `.gitignore`.
- An unrequired SMB signing setting does not prove unsigned sessions, viable NTLM relay, attacker reachability, or sensitive-share access.
- The baseline is one live model run; E2E scenario results are **mocked LLM/tool runs**, not repeated Duke Gateway evaluations.
- Tool errors, missing data and unsupported assertions should lead to uncertainty or human review rather than an invented risk score.

## Before submission
Complete the human evidence-review record and the real team-contributions/AI-use statements in `docs/TESTING.md` and `docs/DESIGN.md`. Verify paths and commands against the final repository, and attach the original supplied environment document if redistribution is permitted.
