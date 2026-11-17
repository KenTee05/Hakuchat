import unittest
from unittest.mock import patch, Mock
from urllib.parse import quote

from search import web_search
from chat_core import _safe_tool_arguments


class SecurityTests(unittest.TestCase):
    @patch("search.subprocess.run")
    def test_search_passes_query_as_encoded_single_argument(self, mocked_run):
        mocked_run.return_value = Mock(stdout="", returncode=0)
        malicious = "test; touch /tmp/hakkeroitu"
        web_search(malicious)
        args, kwargs = mocked_run.call_args
        command = args[0]
        self.assertIn("q=" + quote(malicious, safe=""), command[-1])
        self.assertNotIn("shell", kwargs)
        self.assertIsInstance(command, list)
        self.assertIn("--max-time", command)

    def test_tool_arguments_are_bounded(self):
        query, count = _safe_tool_arguments(
            '{"query":"Python asyncio","max_results":99}'
        )
        self.assertEqual(query, "Python asyncio")
        self.assertEqual(count, 5)

    def test_invalid_tool_arguments_are_rejected(self):
        with self.assertRaises(ValueError):
            _safe_tool_arguments('{"query":""}')


if __name__ == "__main__":
    unittest.main()
