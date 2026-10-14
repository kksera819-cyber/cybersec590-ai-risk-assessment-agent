"""Baseline deterministic demonstration, not yet an LLM-driven agent."""
import json
from datetime import datetime, timezone
from pathlib import Path
from .tools import lookup_environment
from .risk_policy import rate

ROOT = Path(__file__).resolve().parents[1]

def main():
    threat = json.loads((ROOT / 'data/threat_input.json').read_text(encoding='utf-8'))
    env = lookup_environment(threat['asset_id'])
    # Weakness confirmed, but exploitation prerequisites and file sensitivity unknown.
    policy = rate('unknown', 'unknown')
    result = {
        'case_id': threat['case_id'], 'asset_id': threat['asset_id'],
        'threat': threat['threat'], 'decision': policy['decision'],
        'policy_rule': policy['rule'],
        'confirmed_facts': ['FILE04 does not require SMB signing', 'SMB1 disabled in W05 cohort'],
        'unknowns': ['Whether relay prerequisites and network path exist', 'FILE04 data classification'],
        'evidence': env.get('evidence', []), 'source_mode': 'simulated',
        'confidence': 'limited',
        'recommended_action': 'Verify effective signing and NTLM configuration, network paths, and share sensitivity; require SMB signing where feasible.',
        'evidence_to_resolve': ['SMB server/client configuration', 'Firewall/flow records', 'Share access and classification'],
        'review_status': 'pending_human_review',
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'implementation_status': 'baseline_only_no_llm_tool_call'
    }
    output = ROOT / 'outputs/assessment.json'
    output.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
