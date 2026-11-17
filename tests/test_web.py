"""Synthetic markup fixtures test extraction and URL boundaries, not Urdu accuracy."""
import importlib.util
from pathlib import Path

import pytest

pytest.importorskip("lxml")
spec = importlib.util.spec_from_file_location(
    "crawl_wikimedia", Path(__file__).resolve().parents[1] / "scripts/crawl_wikimedia.py")
web = importlib.util.module_from_spec(spec)
spec.loader.exec_module(web)


def test_allowlist():
    assert web.allowed_url("https://ur.wikisource.org/wiki/Test")
    assert not web.allowed_url("https://other.example/wiki/Test")
    assert not web.allowed_url("https://ur.wikisource.org/w/api.php")
    assert not web.allowed_url("https://ur.wikisource.org/wiki/Test?oldid=1")


def test_extract_retains_revision_and_removes_script():
    body = ('<h1 id="firstHeading">Fixture</h1><div class="mw-parser-output">'
            '<script>unwanted</script><p>' + '\u0627' * 110 + '</p></div>'
            '<a href="/w/index.php?oldid=42">Revision</a>'
            '<div id="footer-info-copyright"><a href="/Terms_of_Use">Creative Commons Terms</a></div>')
    row = web.extract(body.encode(), "https://ur.wikisource.org/wiki/Fixture")
    assert row["source"]["revision_id"] == 42
    assert "unwanted" not in row["text"]
    assert row["review_status"] == "unreviewed"
    with pytest.raises(ValueError, match="licensing"):
        web.extract(b'<div class="mw-parser-output">Fixture</div>',
                    "https://ur.wikisource.org/wiki/Fixture")
