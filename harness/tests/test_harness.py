"""Offline tests: retry policy, format re-request, parsing, prompts, citation index.

Run from the repo root:  python -m unittest discover -s harness/tests -t .
"""
import io
import json
import unittest
import urllib.error

from harness import providers
from harness.parse import ParseError, parse_reply
from harness.prompts import case_prompt, make_batches
from harness.run import ask_once
from harness.sources import check_citation, rule_text_9b2


class FakeResp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def http_error(code, body="", retry_after=None):
    hdrs = {"retry-after": retry_after} if retry_after else {}
    return urllib.error.HTTPError("https://x", code, "err", hdrs, io.BytesIO(body.encode()))


class RetryTests(unittest.TestCase):
    def test_retries_429_and_5xx_then_succeeds(self):
        seq = [http_error(429), http_error(503), FakeResp(b'{"ok": 1}')]
        def opener(req, timeout):
            x = seq.pop(0)
            if isinstance(x, Exception):
                raise x
            return x
        stats, slept = providers.CallStats(), []
        out = providers.http_json("GET", "https://x", stats=stats, opener=opener, sleep=slept.append)
        self.assertEqual(out, {"ok": 1})
        self.assertEqual(stats.transport_retries, 2)       # counted, but not as answer attempts
        self.assertEqual(len(slept), 2)

    def test_honors_retry_after(self):
        seq = [http_error(429, retry_after="7"), FakeResp(b"{}")]
        def opener(req, timeout):
            x = seq.pop(0)
            if isinstance(x, Exception):
                raise x
            return x
        slept = []
        providers.http_json("GET", "https://x", opener=opener, sleep=slept.append)
        self.assertEqual(slept, [7.0])

    def test_does_not_retry_400(self):
        def opener(req, timeout):
            raise http_error(400, "bad request")
        with self.assertRaises(providers.TransportError):
            providers.http_json("GET", "https://x", opener=opener, sleep=lambda s: None)


class FakeProvider:
    """Replays canned replies so ask_once can be tested without a network."""
    def __init__(self, replies):
        self.replies, self.turns_seen = list(replies), []

    def chat(self, model, turns, stats):
        self.turns_seen.append(list(turns))
        return self.replies.pop(0)


class AskOnceTests(unittest.TestCase):
    good = json.dumps({"label": "violates", "reasoning": "r.", "citation": "12 CFR 1002.9(b)(2)", "deciding_fact": None})

    def test_first_reply_ok(self):
        rec = ask_once(FakeProvider([self.good]), "m", "prompt")
        self.assertEqual(rec["parse_status"], "ok")
        self.assertFalse(rec["format_rerequest"])

    def test_one_format_only_rerequest(self):
        p = FakeProvider(["I think it violates.", self.good])
        rec = ask_once(p, "m", "prompt")
        self.assertEqual(rec["parse_status"], "ok_after_rerequest")
        self.assertEqual(len(p.turns_seen), 2)
        self.assertIn("could not be parsed", p.turns_seen[1][-1]["content"])

    def test_still_unparseable_is_a_miss(self):
        rec = ask_once(FakeProvider(["nope", "still nope"]), "m", "prompt")
        self.assertEqual(rec["parse_status"], "unparseable")
        self.assertIsNone(rec["parsed"])


class ParseTests(unittest.TestCase):
    def test_fenced_json(self):
        p = parse_reply('```json\n{"label": "Depends", "reasoning": "x", "citation": "c", "deciding_fact": "y"}\n```')
        self.assertEqual(p["label"], "depends")

    def test_bad_label(self):
        with self.assertRaises(ParseError):
            parse_reply('{"label": "unclear"}')


class PromptAndSourceTests(unittest.TestCase):
    def test_condition_a_has_rule_only(self):
        a, b = case_prompt("facts", "A"), case_prompt("facts", "B")
        self.assertIn(rule_text_9b2(), a)
        self.assertNotIn("Combined credit scoring and judgmental system", a)
        self.assertIn("Combined credit scoring and judgmental system", b)
        c = case_prompt("facts", "C")
        self.assertIn("Third parties.", c)            # comment 9(g)-1 is only in the full rulebook
        self.assertIn("Current delinquency or default.", c)

    def test_batches_cover_all_cases_once(self):
        cases = [{"id": f"C{i:02d}", "facts": "f", "seam": f"S{i % 7}"} for i in range(30)]
        batches = make_batches(cases, 5)
        ids = [c["id"] for b in batches for c in b]
        self.assertEqual(sorted(ids), sorted(c["id"] for c in cases))
        self.assertTrue(all(len(b) == 5 for b in batches))

    def test_citation_index(self):
        ok = check_citation("12 CFR 1002.9(b)(2); comments 9(b)(2)-2, 9(b)(2)-7; appendix C, para. 4")
        self.assertEqual(ok["missing"], [])
        bad = check_citation("comment 9(b)(2)-12; CFPB Circular 2023-03")
        self.assertEqual(bad["missing"], ["comment 9(b)(2)-12"])
        self.assertTrue(bad["withdrawn"])


if __name__ == "__main__":
    unittest.main()
