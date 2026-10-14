"""Deterministic, mocked-model full agent orchestration tests; no Duke API calls.
Run: python -m scripts.run_e2e_tests
"""
import json
from pathlib import Path
from types import SimpleNamespace
from src.agent import run
from src.tools import REFERENCE

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'data' / 'threat_input.json'
OUT = ROOT / 'outputs' / 'e2e_tests'

class MockMessage:
    def __init__(self, calls=None, content=None):
        self.tool_calls = calls
        self.content = content
    def model_dump(self, exclude_none=True):
        if self.tool_calls:
            return {'role': 'assistant', 'tool_calls': [{'id': c.id, 'type': 'function', 'function': {'name': c.function.name, 'arguments': c.function.arguments}} for c in self.tool_calls]}
        return {'role': 'assistant', 'content': self.content}

class MockClient:
    def __init__(self, proposed):
        self.proposed = proposed
        self.count = 0
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self.create))
    def create(self, **kwargs):
        self.count += 1
        if self.count == 1:
            calls = [SimpleNamespace(id='call_env', function=SimpleNamespace(name='lookup_environment', arguments=json.dumps({'asset_id': 'FILE04'}))), SimpleNamespace(id='call_ref', function=SimpleNamespace(name='lookup_external_reference', arguments=json.dumps({'url': REFERENCE})))]
            msg = MockMessage(calls=calls)
        else:
            msg = MockMessage(content=json.dumps({'applicability': self.proposed[0], 'impact': self.proposed[1], 'rationale': 'Controlled synthetic fixture; not an observed production risk.', 'unknowns': [], 'recommended_action': 'Review the simulated configuration.', 'evidence_to_resolve': []}))
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])

def fixture_dispatch(config):
    def execute(name, args):
        if name == 'lookup_environment':
            if args.get('asset_id') != 'FILE04':
                return {'status': 'not_found', 'asset_id': args.get('asset_id')}
            if config.get('missing_env'):
                return {'status': 'unavailable', 'source_mode': 'simulated_test'}
            return {'status': 'ok', 'source_mode': 'simulated_test', 'asset': {'id': 'FILE04', 'network_reachability_for_relay': config.get('reachability'), 'ntlm_relay_prerequisites_met': config.get('prerequisites'), 'sensitive_share_access': config.get('sensitive')}, 'evidence': [{'id': 'TEST', 'fact': 'Synthetic evidence for controlled test', 'source_mode': 'simulated_test'}], 'context_evidence': []}
        if name == 'lookup_external_reference':
            if config.get('external_failure'):
                return {'status': 'unavailable', 'url': REFERENCE, 'source_mode': 'simulated_failure', 'error_type': 'SimulatedTimeout'}
            return {'status': 'ok', 'url': REFERENCE, 'source_mode': 'simulated_test', 'content_excerpt': 'SMB signing protects message integrity.'}
        return {'status': 'invalid_tool'}
    return execute

SCENARIOS = [
    ('T1_confirmed', ('confirmed', 'high'), {'reachability': True, 'prerequisites': True, 'sensitive': True}, 'High'),
    ('T1_not_applicable', ('not_applicable', 'high'), {'reachability': False, 'prerequisites': False, 'sensitive': True}, 'Low'),
    ('T2_high_impact', ('confirmed', 'high'), {'reachability': True, 'prerequisites': True, 'sensitive': True}, 'High'),
    ('T2_low_impact', ('confirmed', 'low'), {'reachability': True, 'prerequisites': True, 'sensitive': False}, 'Medium'),
    ('T3_missing_evidence', ('confirmed', 'high'), {'missing_env': True}, 'Insufficient Evidence'),
    ('T4_external_failure', ('confirmed', 'high'), {'reachability': True, 'prerequisites': True, 'sensitive': True, 'external_failure': True}, 'Insufficient Evidence'),
]

def execute_all(output_root=OUT):
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)
    report = []
    for name, proposed, fixture, expected in SCENARIOS:
        dest = output_root / name
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'fixture.json').write_text(json.dumps({'proposed_model_analysis': {'applicability': proposed[0], 'impact': proposed[1]}, 'simulated_tool_conditions': fixture, 'expected_decision': expected}, indent=2), encoding='utf-8')
        result = run(client=MockClient(proposed), model='mock-model-for-e2e', case_path=CASE, output_dir=dest, dispatch_fn=fixture_dispatch(fixture))
        trace = json.loads((dest / 'agent_trace.json').read_text(encoding='utf-8'))
        tool_names = [item['tool'] for item in trace['tool_trace']]
        passed = (result['decision'] == expected and result['tool_checks']['environment_called'] == (not fixture.get('missing_env', False)) and result['tool_checks']['external_called'] and 'lookup_environment' in tool_names and 'lookup_external_reference' in tool_names)
        report.append({'scenario': name, 'expected': expected, 'actual': result['decision'], 'pass': passed, 'mode': 'mock_model_and_simulated_tools'})
    (output_root / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    lines = ['# End-to-End Agent Orchestration Tests', '', 'Mode: deterministic mocked LLM and simulated tools; these are NOT live Duke Gateway evaluations.', '', '| Scenario | Expected | Actual | Result |', '|---|---|---|---|']
    for r in report:
        lines.append(f"| {r['scenario']} | {r['expected']} | {r['actual']} | {'PASS' if r['pass'] else 'FAIL'} |")
    lines += ['', 'Each scenario directory contains fixture.json, agent_assessment.json, and agent_trace.json.', 'The live Duke Gateway baseline remains in outputs/baseline/.']
    (output_root / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    return report

if __name__ == '__main__':
    results = execute_all()
    for item in results:
        print(f"{item['scenario']}: expected={item['expected']}, actual={item['actual']}, {'PASS' if item['pass'] else 'FAIL'}")
    print(f"Summary: {sum(r['pass'] for r in results)}/{len(results)} passed; outputs: {OUT}")
    if not all(r['pass'] for r in results):
        raise SystemExit(1)
