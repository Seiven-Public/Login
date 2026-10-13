import importlib.util
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import tempfile
import unittest


SPEC = importlib.util.spec_from_file_location(
    "generate_readme", Path(__file__).resolve().parents[1] / "scripts/generate_readme.py"
)
catalogue = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalogue)

BEGIN = "<!-- BEGIN IMAGE CATALOG -->"
END = "<!-- END IMAGE CATALOG -->"


class GalleryHTML(HTMLParser):
    def __init__(self, content):
        super().__init__()
        self.tags = []
        self.text = []
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

    def handle_data(self, data):
        self.text.append(data)


class TrackedImagesTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "--quiet")

    def git(self, *args):
        subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            capture_output=True,
        )

    def write(self, name, tracked=True):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
        if tracked:
            self.git("add", "--", name)

    def test_recursively_lists_only_existing_tracked_images(self):
        extensions = ["apng", "avif", "bmp", "gif", "ico", "jpeg", "jpg", "png", "svg", "webp"]
        expected = {f"images/deep/photo.{ext.upper()}" for ext in extensions}
        expected.add("images/été espace #1? | image.png")
        for name in expected:
            self.write(name)
        self.write("README.md")
        self.write("images/notes.png.txt")
        self.write("images/untracked.png", tracked=False)
        self.write("images/missing.png")
        (self.root / "images/missing.png").unlink()
        (self.root / "images/link.png").symlink_to("deep/photo.PNG")
        self.git("add", "--", "images/link.png")

        self.assertEqual(set(catalogue.image_paths(self.root)), expected)

    def test_addition_and_deletion_are_reflected_on_next_generation(self):
        self.write("first.png")
        self.assertEqual(catalogue.image_paths(self.root), ["first.png"])
        self.write("new folder/second.webp")
        self.git("rm", "--force", "--", "first.png")
        self.assertEqual(catalogue.image_paths(self.root), ["new folder/second.webp"])

    def test_repository_without_images_has_empty_catalogue(self):
        self.write("README.md")
        self.assertEqual(catalogue.image_paths(self.root), [])


class GalleryTests(unittest.TestCase):
    def test_raw_url_encodes_branch_and_filename_without_flattening_directories(self):
        self.assertEqual(
            catalogue.image_url("Seiven-Public/Login", "feature/gallery", "images/été #1? | photo.png"),
            "https://raw.githubusercontent.com/Seiven-Public/Login/feature%2Fgallery/"
            "images/%C3%A9t%C3%A9%20%231%3F%20%7C%20photo.png",
        )

    def test_gallery_has_thumbnail_raw_link_and_copyable_url_for_each_image(self):
        paths = ["logos/été #1? | image.PNG", "banners/hero.webp"]
        rendered = catalogue.render_gallery(paths, "Seiven-Public/Login", "main")
        parsed = GalleryHTML(rendered)
        self.assertTrue(any(tag == "table" for tag, _ in parsed.tags))
        thumbnails = [attrs for tag, attrs in parsed.tags if tag == "img"]
        self.assertEqual(len(thumbnails), len(paths))
        links = {attrs.get("href") for tag, attrs in parsed.tags if tag == "a"}
        for path, thumbnail in zip(paths, thumbnails):
            url = catalogue.image_url("Seiven-Public/Login", "main", path)
            self.assertEqual(thumbnail.get("src"), url)
            self.assertEqual(thumbnail.get("width"), "140")
            self.assertIn(url, links)
            self.assertIn(f"```text\n{url}\n```", rendered)

    def test_filenames_cannot_inject_html(self):
        path = 'images/<script>alert("x")</script> & logo.png'
        rendered = catalogue.render_gallery([path], "Seiven-Public/Login", "main")
        parsed = GalleryHTML(rendered)
        self.assertFalse(any(tag == "script" for tag, _ in parsed.tags))
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("&amp;", rendered)
        self.assertIn(path, "".join(parsed.text))

    def test_empty_gallery_does_not_render_broken_thumbnails(self):
        rendered = catalogue.render_gallery([], "Seiven-Public/Login", "main")
        self.assertIsInstance(rendered, str)
        self.assertFalse(any(tag == "img" for tag, _ in GalleryHTML(rendered).tags))


class ReadmeUpdateTests(unittest.TestCase):
    def test_only_generated_section_changes_and_second_run_is_identical(self):
        prefix = "# Login\n\nTexte manuel à préserver.\n\n"
        suffix = "\n\n## Contribution\nLes consignes restent ici.\n"
        source = f"{prefix}{BEGIN}\nancien contenu\n{END}{suffix}"
        updated = catalogue.update_readme(source, "nouveau catalogue")
        actual_prefix, generated = updated.split(BEGIN)
        gallery, actual_suffix = generated.split(END)
        self.assertEqual(actual_prefix, prefix)
        self.assertEqual(actual_suffix, suffix)
        self.assertEqual(gallery.strip(), "nouveau catalogue")
        self.assertEqual(catalogue.update_readme(updated, "nouveau catalogue"), updated)

    def test_invalid_markers_fail_instead_of_overwriting_manual_content(self):
        for source in [
            "Texte manuel sans marqueur",
            BEGIN,
            END,
            f"{END}\n{BEGIN}",
            f"{BEGIN}\n{BEGIN}\n{END}",
            f"{BEGIN}\n{END}\n{END}",
            f"{BEGIN}\n{END}\n{BEGIN}\n{END}",
        ]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                catalogue.update_readme(source, "nouveau catalogue")


if __name__ == "__main__":
    unittest.main()
