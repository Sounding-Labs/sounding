import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from check_markdown_links import check, main


class MarkdownLinksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="markdown-links-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content=""):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_resolves_from_source_directory_and_checks_images(self):
        self.write("docs/nested/page.md", "[API](../api.md#errors) ![art](../../assets/art.svg)")
        self.write("docs/api.md")
        self.write("assets/art.svg")
        self.assertEqual(check(self.root), (2, 2, []))

    def test_missing_link_fails_and_names_file_and_target(self):
        self.write("docs/page.md", "Heading\n[missing](gone.md)")
        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr):
            self.assertEqual(main([str(self.root)]), 1)
        self.assertIn("docs/page.md:2: broken relative link: gone.md", stderr.getvalue())

    def test_absolute_urls_and_anchors_never_fetch(self):
        self.write("page.md", "[HTTPS](https://invalid.invalid/a) [HTTP](http://invalid.invalid) "
                   "[here](#absent) [email](mailto:nobody@example.invalid) [cdn](//invalid.invalid/x) "
                   "[unreachable](https://[invalid)")
        with patch("socket.socket", side_effect=AssertionError("network used")):
            self.assertEqual(check(self.root), (1, 0, []))

    def test_reference_links_and_titles(self):
        self.write("docs/page.md", '[manual][guide]\n[guide]: ../manual.md "Guide"\n[missing]: absent.md\n')
        self.write("manual.md")
        self.assertEqual(check(self.root)[2], [("docs/page.md", 3, "absent.md")])

    def test_spaces_encoded_paths_parentheses_and_root_paths(self):
        self.write("docs/page.md", '[a](<../space name.md> "title") [b](../encoded%20name.md) '
                   '[c](../name(nested).md) [d](/space%20name.md)')
        for name in ("space name.md", "encoded name.md", "name(nested).md"):
            self.write(name)
        self.assertEqual(check(self.root), (4, 4, []))

    def test_code_and_comments_are_not_links(self):
        self.write("page.md", '`[inline](missing.md)`\n```md\n[code](missing.md)\n```\n'
                   '~~~\n[other](missing.md)\n~~~\n<!-- [hidden](missing.md) -->\n')
        self.assertEqual(check(self.root), (1, 0, []))

    def test_html_links_are_checked(self):
        self.write("page.md", '<a href="docs/ok.md">ok</a> <img src="gone.svg">')
        self.write("docs/ok.md")
        self.assertEqual(check(self.root)[2], [("page.md", 1, "gone.svg")])

    def test_scans_nested_and_hidden_markdown_but_not_git(self):
        self.write(".github/guide.md", "[bad](gone.md)")
        self.write("docs/a/b/page.md", "[bad](gone.md)")
        self.write(".git/ignored.md", "[bad](gone.md)")
        files, checked, broken = check(self.root)
        self.assertEqual((files, checked, len(broken)), (2, 2, 2))

    def test_success_and_missing_root(self):
        self.write("page.md", "[self](page.md)")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([str(self.root)]), 0)
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as error:
            main([str(self.root / "absent")])
        self.assertEqual(error.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
