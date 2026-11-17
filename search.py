"""DuckDuckGo HTML -haku curl-komennolla."""
from __future__ import annotations

import json
import subprocess
import sys
from html.parser import HTMLParser
from urllib.parse import parse_qs, quote, urlparse


MAX_QUERY_LENGTH = 300
MAX_TITLE_LENGTH = 200
MAX_RESULTS_LIMIT = 10


class _ResultsParser(HTMLParser):
    """Poimii DuckDuckGon tuloslinkit; sivun muu teksti ohitetaan."""

    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._in_result = False
        self._title_parts: list[str] = []
        self._href = ""

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = dict(attrs)
        classes = attrs_dict.get("class", "").split()
        if tag == "a" and "result__a" in classes:
            self._in_result = True
            self._href = attrs_dict.get("href", "")
            self._title_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_result:
            self._title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._in_result:
            title = " ".join("".join(self._title_parts).split())[:MAX_TITLE_LENGTH]
            href = self._normalize_url(self._href)
            if title and href and href.startswith(("http://", "https://")):
                self.results.append({"title": title, "url": href})
            self._in_result = False
            self._href = ""
            self._title_parts = []

    @staticmethod
    def _normalize_url(href: str) -> str:
        parsed = urlparse(href)
        if parsed.hostname and parsed.hostname.endswith("duckduckgo.com"):
            target = parse_qs(parsed.query).get("uddg", [""])[0]
            return target
        return href


def parse_search_results(html: str, max_results: int = 5) -> list[dict[str, str]]:
    parser = _ResultsParser()
    parser.feed(html)
    # Poista saman URL:n toistot ja rajoita palautettavan datan kokoa.
    unique: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in parser.results:
        if item["url"] not in seen:
            unique.append(item)
            seen.add(item["url"])
        if len(unique) >= max_results:
            break
    return unique


def web_search(query: str, max_results: int = 5) -> list[dict[str, str]]:
    """Hakee verkosta otsikot ja URL-osoitteet DuckDuckGon HTML-haulla."""
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Hakusana ei saa olla tyhjä.")
    query = query.strip()[:MAX_QUERY_LENGTH]
    if isinstance(max_results, bool) or not isinstance(max_results, int):
        max_results = 5
    max_results = max(1, min(max_results, MAX_RESULTS_LIMIT))

    url = "https://html.duckduckgo.com/html/?q=" + quote(query, safe="")
    try:
        completed = subprocess.run(
            ["curl", "-fsSL", "--max-time", "10", "-A", "Mozilla/5.0", url],
            capture_output=True,
            text=True,
            timeout=12,
            check=True,
        )
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        raise RuntimeError("Verkkohaku epäonnistui. Tarkista verkkoyhteys ja curl.") from exc

    return parse_search_results(completed.stdout[:1_000_000], max_results)


if __name__ == "__main__":
    term = " ".join(sys.argv[1:]).strip()
    if not term:
        print('Käyttö: python search.py "WSL2 Docker"')
        raise SystemExit(2)
    try:
        print(json.dumps(web_search(term), ensure_ascii=False, indent=2))
    except (ValueError, RuntimeError) as exc:
        print(f"Hakuvirhe: {exc}", file=sys.stderr)
        raise SystemExit(1)
