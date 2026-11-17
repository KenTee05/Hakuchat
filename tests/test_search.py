import unittest

from search import parse_search_results


class SearchParserTests(unittest.TestCase):
    def test_extracts_and_limits_results(self):
        html = """
        <a class="result__a" href="https://example.com/a">Example A</a>
        <a class="result__a" href="https://example.com/b">Example B</a>
        """
        self.assertEqual(
            parse_search_results(html, 1),
            [{"title": "Example A", "url": "https://example.com/a"}],
        )

    def test_unwraps_duckduckgo_redirect(self):
        html = '<a class="result__a" href="//duckduckgo.com/l/?uddg=https%3A%2F%2Fexample.org%2F">Site</a>'
        self.assertEqual(
            parse_search_results(html),
            [{"title": "Site", "url": "https://example.org/"}],
        )

    def test_ignores_non_result_links(self):
        html = '<a href="https://example.com">Not a result</a>'
        self.assertEqual(parse_search_results(html), [])


if __name__ == "__main__":
    unittest.main()
