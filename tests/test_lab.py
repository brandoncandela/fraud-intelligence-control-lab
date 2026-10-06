import json
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FraudLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from src.generate_lab import build
        cls.export = build()
        cls.con = sqlite3.connect(ROOT / "dist" / "data" / "lab.sqlite")

    @classmethod
    def tearDownClass(cls):
        cls.con.close()

    def test_foreign_keys_are_clean(self):
        self.assertEqual(self.con.execute("PRAGMA foreign_key_check").fetchall(), [])

    def test_expected_population(self):
        self.assertEqual(self.export["totals"]["accounts"], 60)
        self.assertEqual(self.export["totals"]["review_worthy"], 7)
        self.assertGreater(self.export["totals"]["transactions"], 3700)

    def test_mule_cluster_is_linked(self):
        rows = self.con.execute("SELECT account_id FROM account_devices WHERE device_id='D900'").fetchall()
        self.assertEqual(len(rows), 5)

    def test_threshold_tradeoff_is_present(self):
        rows = self.export["accounts"]
        loose = [r for r in rows if r["risk_score"] >= 25]
        strict = [r for r in rows if r["risk_score"] >= 50]
        self.assertGreater(len(loose), len(strict))
        self.assertTrue(any(r["outcome"] == "benign" for r in loose))
        self.assertTrue(any(r["outcome"] == "review_worthy" and r not in strict for r in rows))

    def test_account_takeover_feature(self):
        rows = {r["account_id"]: r for r in self.export["accounts"]}
        self.assertGreater(rows["A041"]["new_foreign_device_amount"], 8000)
        self.assertGreater(rows["A052"]["new_foreign_device_amount"], 10000)

    def test_benign_marketplace_lookalike(self):
        row = next(r for r in self.export["accounts"] if r["account_id"] == "A015")
        self.assertEqual(row["outcome"], "benign")
        self.assertGreaterEqual(row["distinct_in_senders_24h"], 8)

    def test_export_is_valid_json(self):
        disk = json.loads((ROOT / "dist" / "data" / "dashboard.json").read_text())
        self.assertEqual(disk["totals"], self.export["totals"])


if __name__ == "__main__":
    unittest.main()
