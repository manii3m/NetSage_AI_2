import unittest
from src.checker import check_rules
import pandas as pd
from pathlib import Path

class TestRuleChecker(unittest.TestCase):
    def setUp(self):
        # Load the CSV data to run tests against
        data_path = Path(__file__).parent.parent / "data" / "cases.csv"
        self.df = pd.read_csv(data_path)

    def test_administratively_down(self):
        case = self.df[self.df['case_id'] == 'NET-001'].iloc[0].to_dict()
        result = check_rules(case)
        self.assertEqual(result['status'], 'ERRORS_DETECTED')
        self.assertEqual(len(result['findings']), 1)
        self.assertEqual(result['findings'][0]['type'], 'INTERFACE_ADMINISTRATIVELY_DOWN')

    def test_mtu_mismatch(self):
        case = self.df[self.df['case_id'] == 'NET-002'].iloc[0].to_dict()
        result = check_rules(case)
        self.assertEqual(result['status'], 'ERRORS_DETECTED')
        self.assertTrue(any(f['type'] == 'MTU_MISMATCH' for f in result['findings']))

    def test_nat_overload_missing(self):
        case = self.df[self.df['case_id'] == 'NET-003'].iloc[0].to_dict()
        result = check_rules(case)
        self.assertEqual(result['status'], 'ERRORS_DETECTED')
        self.assertTrue(any(f['type'] == 'NAT_INDICATORS' for f in result['findings']))

    def test_dhcp_helper_address(self):
        case = self.df[self.df['case_id'] == 'NET-004'].iloc[0].to_dict()
        result = check_rules(case)
        self.assertEqual(result['status'], 'ERRORS_DETECTED')
        self.assertTrue(any(f['type'] == 'DHCP_PROBLEMS' for f in result['findings']))

    def test_stp_disabled(self):
        case = self.df[self.df['case_id'] == 'NET-005'].iloc[0].to_dict()
        result = check_rules(case)
        self.assertEqual(result['status'], 'ERRORS_DETECTED')
        self.assertTrue(any(f['type'] == 'STP_DISABLED' for f in result['findings']))

    def test_pass_state(self):
        case = {"show_command_output": "Interface Gi0/0 is up, line protocol is up. Everything is fine."}
        result = check_rules(case)
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(len(result['findings']), 0)

if __name__ == '__main__':
    unittest.main()
