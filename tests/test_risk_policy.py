import unittest
from src.risk_policy import rate
from src.tools import lookup_environment, lookup_external_reference

class PolicyTests(unittest.TestCase):
    def test_applicability_change(self):
        self.assertEqual(rate('confirmed', 'high')['decision'], 'High')
        self.assertEqual(rate('not_applicable', 'high')['decision'], 'Low')
    def test_impact_change(self):
        self.assertEqual(rate('confirmed', 'high')['decision'], 'High')
        self.assertEqual(rate('confirmed', 'low')['decision'], 'Medium')
    def test_missing_evidence(self):
        self.assertEqual(rate('unknown', 'high')['decision'], 'Insufficient Evidence')
    def test_invalid_tool_request(self):
        self.assertEqual(lookup_external_reference('https://example.com')['status'], 'blocked')
    def test_environment(self):
        self.assertIs(lookup_environment('FILE04')['asset']['smb_signing_required'], False)

if __name__ == '__main__':
    unittest.main()
