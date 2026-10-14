"""Runs deterministic mock-model full-agent scenarios in a temporary directory."""
import tempfile
import unittest
from pathlib import Path
from scripts.run_e2e_tests import execute_all

class AgentEndToEndTests(unittest.TestCase):
    def test_six_controlled_runs(self):
        with tempfile.TemporaryDirectory() as temp:
            results = execute_all(Path(temp))
            self.assertEqual(len(results), 6)
            for result in results:
                with self.subTest(scenario=result['scenario']):
                    self.assertTrue(result['pass'], result)

if __name__ == '__main__':
    unittest.main()
