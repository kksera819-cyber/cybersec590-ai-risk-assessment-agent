import unittest
from unittest.mock import patch
from src.risk_policy import rate
from src.tools import lookup_external_reference, _clean_markdown

class UpgradeTests(unittest.TestCase):
    def test_applicability_change(self):
        self.assertEqual(rate('potential', 'medium')['decision'], 'Medium')
        self.assertEqual(rate('confirmed', 'medium')['decision'], 'High')

    def test_impact_change(self):
        self.assertEqual(rate('potential', 'low')['decision'], 'Low')
        self.assertEqual(rate('potential', 'high')['decision'], 'Medium')

    def test_missing_evidence(self):
        self.assertEqual(rate('unknown', 'medium')['decision'], 'Insufficient Evidence')

    def test_external_failure(self):
        with patch('src.tools.urlopen', side_effect=TimeoutError('controlled failure')):
            response = lookup_external_reference('https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview')
        self.assertEqual(response['status'], 'unavailable')
        self.assertNotEqual(response['status'], 'ok')

    def test_html_rejected(self):
        class FakeResponse:
            headers = {'Content-Type': 'text/html'}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, count): return b'<!DOCTYPE html><html><head>SMB</head></html>'
        with patch('src.tools.urlopen', return_value=FakeResponse()):
            response = lookup_external_reference('https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-signing-overview')
        self.assertEqual(response['status'], 'unavailable')

if __name__ == '__main__':
    unittest.main()
