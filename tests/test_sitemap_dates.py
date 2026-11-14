import os
from pathlib import Path
import tempfile
import unittest

from sitemap_dates import content_dates, fingerprint


class SitemapDatesTest(unittest.TestCase):
    def test_build_timestamps_and_asset_versions_do_not_change_dates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / 'index.html'
            page.write_text('<head>\n<title>A</title>\n</head><p>Hello</p><script src="app.js?v=42"></script>')
            state = root / 'dates.json'
            pages = {'/': page}
            self.assertEqual(content_dates(pages, state, '2026-11-13'), {'/': '2026-11-13'})
            os.utime(page, (1900000000, 1900000000))
            page.write_text(page.read_text().replace('v=42', 'v=43').replace('<title>', '\n\n<title>'))
            self.assertEqual(content_dates(pages, state, '2026-11-14'), {'/': '2026-11-13'})
            page.write_text(page.read_text().replace('Hello', 'New content'))
            self.assertEqual(content_dates(pages, state, '2026-11-15'), {'/': '2026-11-15'})
            self.assertEqual(content_dates(pages, state, '2026-11-16'), {'/': '2026-11-15'})
            other = root / 'other.html'
            other.write_text('<p>New page</p>')
            self.assertEqual(content_dates({'/new': other}, state, '2026-11-16'), {'/new': '2026-11-16'})

    def test_body_whitespace_and_metadata_changes_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / 'page.html'
            page.write_text('<head><title>A</title></head><pre>A\n\nB</pre>')
            original = fingerprint(page)
            page.write_text(page.read_text().replace('<title>A', '<title>B'))
            self.assertNotEqual(fingerprint(page), original)
            original = fingerprint(page)
            page.write_text(page.read_text().replace('A\n\nB', 'A\nB'))
            self.assertNotEqual(fingerprint(page), original)


if __name__ == '__main__':
    unittest.main()
