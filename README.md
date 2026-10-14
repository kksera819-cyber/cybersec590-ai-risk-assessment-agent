# Assignment 2 – SMB Relay Risk Assessment Agent

## Project Overview

For this assignment, I built a Python agent to assess a possible SMB relay risk on FILE04, a Windows Server 2022 file server in the simulated Northbridge Services environment.

**Risk question:** Does FILE04 not requiring SMB signing create a meaningful SMB relay risk in this environment?

The agent uses the Duke AI Gateway to choose and call tools. It checks the simulated environment data and a Microsoft Learn reference, then uses a Python risk policy to make the final decision. This is a risk assessment exercise, not a penetration test.

### Main Result

The saved live agent run returned:

| Field | Result |
|---|---|
| Applicability | `potential` |
| Impact | `unknown` |
| Decision | `Insufficient Evidence` |
| Policy rule | `P1: decisive evidence missing` |

FILE04 does not require SMB signing, but the available data does not confirm internal SMB reachability, NTLM relay prerequisites, or the sensitivity of its shared files. Because of these unknowns, the agent does not assign a High, Medium, or Low rating.

## Setup

Use Python 3.10 or newer. From the project folder, install the dependencies:

```powershell
python -m pip install -r requirements-agent.txt
```

Create a `.env` file in the project root:

```dotenv
LITELLM_TOKEN=YOUR_DUKE_GATEWAY_TOKEN
DUKE_GATEWAY_URL=https://litellm.oit.duke.edu/v1
DUKE_MODEL=gpt-6-luna
```

A valid Duke AI Gateway token and network access are required for a live run. **Do not upload the `.env` file or your token to GitHub.**

## How to Run

Run these commands from the project root:

```powershell
# Run the agent using Duke AI Gateway
python -m src.agent

# Run unit tests
python -m unittest discover -s tests -v

# Run the mocked end-to-end scenarios
python -m scripts.run_e2e_tests
```

The agent saves its assessment to `outputs/agent_assessment.json` and its tool trace to `outputs/agent_trace.json`.

## Testing Results

The recorded tests passed:

| Test | Result |
|---|---|
| Unit tests | 11 passed |
| Mocked end-to-end scenarios | 6 passed |
| Live Duke AI Gateway baseline | Completed |

The six end-to-end scenarios test changes in applicability and impact, missing evidence, and an external tool failure. They use mocked model/tool responses so the results are repeatable. **They are not six separate live Gateway runs.**

Test files and saved results are available in `tests/`, `outputs/e2e_tests/`, and `outputs/baseline/`.

## Project Files

| Path | Purpose |
|---|---|
| `data/environment.json` | Simulated environment and evidence |
| `data/threat_input.json` | Threat scenario and risk question |
| `src/agent.py` | Agent workflow and tool calling |
| `src/tools.py` | Environment and external reference lookups |
| `src/risk_policy.py` | Risk rating rules |
| `tests/` | Unit and agent tests |
| `scripts/run_e2e_tests.py` | End-to-end test runner |
| `outputs/` | Assessments, traces, and test results |

## Documentation

- [Design and risk policy](docs/DESIGN.md)
- [Testing plan](docs/TESTING.md)
- [Test results](docs/test_results.md)
- [Architecture diagram](docs/architecture.mmd)
- [Human evidence self-review](docs/HUMAN_REVIEW.md)

## Evidence and Limitations

The environment evidence is simulated and based on the provided `Windows_Enterprise_Environment.docx` (September 23, 2026 snapshot). S02, S03, and S05 are evidence IDs from that scenario.

The agent also looks up Microsoft's [SMB signing documentation](https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview). This reference explains the security issue, but it does not prove that FILE04 can be exploited.

The project does not test a real network or attempt an SMB relay attack. Missing information is kept as unknown instead of being treated as confirmed risk. The saved assessment was also checked in an individual human evidence self-review.

## Individual Contribution and AI Assistance

I completed this project individually. I worked on the scenario selection, design, Python code, Duke AI Gateway integration, risk policy, tests, documentation, and GitHub submission.

I used AI assistance to help write and debug code, plan tests, and improve the documentation. I checked the environment evidence against the saved agent output and reviewed the final risk decision. I am responsible for the submitted work and its limitations.
