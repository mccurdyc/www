#!/usr/bin/env -S just --justfile
# ^ A shebang isn't required, but allows a justfile to be executed
#   like a script, with `./justfile test`, for example.
#
# Just Manual - https://just.systems/man/en/
# https://just.systems/man/en/working-directory.html
# Settings - https://just.systems/man/en/settings.html
# https://just.systems/man/en/settings.html#bash

set shell := ["/usr/bin/env", "bash", "-uc"]

log := "warn"
export JUST_LOG := log

set quiet := false

shebang := "/usr/bin/env bash"

default: deploy

serve: build
    HUGO_IMAGE_CDN="https://www.mccurdyc.dev" hugo serve --baseURL http://nuc:1313 --bind 0.0.0.0

build: check-submodules
    hugo --ignoreCache
    pagefind --site public

check-submodules:
    @test -f themes/hello-friend-ng/layouts/_default/baseof.html || \
        (echo "Error: theme submodule is not initialized. Run 'git submodule update --init --recursive'" && exit 1)

deploy:
    ./scripts/deploy.sh

rename-seq dir: clean-images
    ./scripts/rename-seq.sh "/mnt/photos/{{ dir }}"

# Usage - just sync-images '2024/early'
sync-images dir:
    just rename-seq {{ dir }}
    gsutil -m rsync -d -r "/mnt/photos/{{ dir }}/" "gs://images.mccurdyc.dev/images/{{ dir }}/"
    gsutil -m rsync -d -r "gs://images.mccurdyc.dev/images/{{ dir }}/" "gs://www.mccurdyc.dev/images/{{ dir }}/"

# Usage - just photo-post '2026/06-bonaire'
photo-post dir:
    just sync-images {{ dir }}
    ./scripts/photo-post.py {{ dir }}

# Remove _L***.jpg images
clean-images:
    find /mnt/photos -name "._*" -exec sudo rm -rf {} \;

# Uploads book cover images to GCS
sync-bookcovers:
    gsutil -m rsync -d -r "/mnt/photos/book-covers" "gs://images.mccurdyc.dev/images/book-covers"

# Import SuperNote digest notes as book posts
import-books:
    ./scripts/supernote-to-book.sh

# List images
list-images dir:
    gsutil ls gs://images.mccurdyc.dev/images/{{ dir }}
