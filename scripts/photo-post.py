#!/usr/bin/env python3
"""Create or update a Hugo photo post from a synced image directory."""

import argparse
import re
import subprocess
import sys
from pathlib import Path

GCS_BASE = "gs://images.mccurdyc.dev"


def run(cmd, **kwargs):
    """Run a subprocess and return its completed process."""
    return subprocess.run(cmd, check=True, text=True, **kwargs)


def list_images(dir_path):
    """Return sorted public image URLs for a directory in GCS."""
    url = f"{GCS_BASE}/images/{dir_path}/"
    result = run(["gsutil", "ls", url], capture_output=True)
    images = sorted(line.strip() for line in result.stdout.splitlines() if line.strip())
    return images


def image_path_from_gcs(gcs_url):
    """Convert a gs:// URL to a site-relative /images/... path."""
    if gcs_url.startswith(GCS_BASE):
        return gcs_url[len(GCS_BASE):]
    return gcs_url


def create_post(post_name):
    """Create the photo post via Hugo if it does not already exist."""
    post_path = Path(f"content/photos/{post_name}.md")
    if not post_path.exists():
        run([
            "hugo", "new", "content", "--kind", "photos",
            f"photos/{post_name}.md",
        ])
    return post_path


def update_frontmatter(post_path, last_image):
    """Set the featured image only when it is still the archetype placeholder."""
    content = post_path.read_text()
    if re.search(r'^image: "/images/"$', content, flags=re.MULTILINE):
        content = re.sub(
            r'^image: "/images/"$',
            f'image: "{last_image}"',
            content,
            flags=re.MULTILINE,
            count=1,
        )
        post_path.write_text(content)


def build_gallery(image_paths):
    """Build the Hugo gallery shortcode block."""
    lines = ["{{< gallery >}}"]
    for path in image_paths:
        lines.append(f'\t{{{{< figure src="{path}" >}}}}')
    lines.extend(["{{< /gallery >}}", "{{< load-photoswipe >}}"])
    return "\n".join(lines) + "\n"


def replace_or_append_gallery(post_path, gallery):
    """Replace an existing gallery block or append one to the post."""
    content = post_path.read_text()
    pattern = r'\n\{\{< gallery >\}\}.*?\{\{< load-photoswipe >\}\}\n?'
    new_content, count = re.subn(pattern, "\n" + gallery, content, flags=re.DOTALL)
    if count == 0:
        new_content = content.rstrip() + "\n\n" + gallery
    post_path.write_text(new_content)


def main():
    parser = argparse.ArgumentParser(
        description="Create or update a photo post from synced images.",
    )
    parser.add_argument(
        "dir",
        help="Photo directory under /mnt/photos (e.g., '2026/06-bonaire')",
    )
    args = parser.parse_args()

    dir_path = args.dir
    post_name = dir_path.replace("/", "-")

    images = list_images(dir_path)
    if not images:
        print(f"error: no images found for {dir_path}", file=sys.stderr)
        sys.exit(1)

    post_path = create_post(post_name)
    image_paths = [image_path_from_gcs(url) for url in images]

    update_frontmatter(post_path, image_paths[-1])
    replace_or_append_gallery(post_path, build_gallery(image_paths))


if __name__ == "__main__":
    main()
