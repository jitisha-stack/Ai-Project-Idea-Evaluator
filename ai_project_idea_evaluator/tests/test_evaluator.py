import unittest
from evaluator import evaluate_idea

class EvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.idea = {"name":"Test idea", "problem":"Test problem", "users":"Students",
            "budget":50000, "annual_benefit":120000, "build_weeks":6, "data_quality":4,
            "team_readiness":4, "maintenance_readiness":3, "risk_level":"Medium",
            "sensitive_data":False, "build_or_buy":"Not sure"}

    def test_score_range(self):
        result = evaluate_idea(self.idea)
        self.assertGreaterEqual(result["score"], 0)
        self.assertLessEqual(result["score"], 100)

    def test_six_pillars(self):
        self.assertEqual(len(evaluate_idea(self.idea)["pillar_scores"]), 6)

    def test_net_benefit(self):
        self.assertEqual(evaluate_idea(self.idea)["net_benefit"], 70000)

    def test_sensitive_data_warning(self):
        result = evaluate_idea(dict(self.idea, sensitive_data=True))
        self.assertTrue(any("sensitive data" in x.lower() for x in result["concerns"]))

if __name__ == "__main__":
    unittest.main()
