import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "email-list-builder" / "scripts" / "build_list.py"
EXAMPLES = ROOT / "examples"

spec = importlib.util.spec_from_file_location("build_list", SCRIPT)
build_list = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_list)


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


class BuildListTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        self.code = build_list.main([
            "--contacts", str(EXAMPLES / "contacts.csv"),
            "--blocklist", str(EXAMPLES / "blocklist.csv"),
            "--already-received", str(EXAMPLES / "already_received.csv"),
            "--exclude-status", "customer,unsubscribed,bounced,do_not_contact",
            "--segments", "brand,supplier,manufacturer",
            "--batch-size", "3",
            "--out", str(self.out),
        ])
        self.send = [r["email"] for r in read_csv(self.out / "send_list.csv")]
        self.excluded = {r["email"]: r["reasons"] for r in read_csv(self.out / "excluded.csv")}
        self.batches = read_csv(self.out / "batches.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def test_all_leak_checks_pass(self):
        self.assertEqual(self.code, 0)
        report = (self.out / "report.md").read_text(encoding="utf-8")
        self.assertIn("ALL CHECKS PASSED", report)
        self.assertNotIn("FAIL:", report)

    def test_expected_send_list(self):
        self.assertEqual(sorted(self.send), sorted([
            "ana.lopez@example.com", "chen.wei@example.net", "jun.park@example.com",
            "kai.meyer@example.org", "maya.singh@example.net", "olga.ivanova@example.org",
        ]))

    def test_duplicates_merged_after_normalisation(self):
        self.assertEqual(self.send.count("ana.lopez@example.com"), 1)

    def test_customer_in_any_history_row_is_excluded(self):
        self.assertIn("status:customer", self.excluded["dana.ito@example.com"])

    def test_blocklist_matches_despite_case_and_spaces(self):
        self.assertIn("blocklist", self.excluded["farah.khan@example.org"])

    def test_other_exclusion_reasons(self):
        self.assertIn("already_received", self.excluded["gio.rossi@example.com"])
        self.assertIn("status:unsubscribed", self.excluded["eli.novak@example.com"])
        self.assertIn("status:bounced", self.excluded["lena.fischer@example.com"])
        self.assertIn("invalid_email", self.excluded["hana.lee@example"])
        self.assertIn("out_of_scope", self.excluded["ivan.petrov@example.net"])
        self.assertIn("out_of_scope", self.excluded["noah.berg@example.com"])

    def test_batches_match_send_list_and_respect_size(self):
        self.assertEqual(sorted(r["email"] for r in self.batches), sorted(self.send))
        sizes = {}
        for r in self.batches:
            sizes[r["batch"]] = sizes.get(r["batch"], 0) + 1
        self.assertTrue(all(n <= 3 for n in sizes.values()))

    def test_segment_priority_order(self):
        order = ["brand", "supplier", "manufacturer"]
        rows = read_csv(self.out / "send_list.csv")
        ranks = [order.index(r["segment"].split(";")[0]) for r in rows]
        self.assertEqual(ranks, sorted(ranks))


if __name__ == "__main__":
    unittest.main()
