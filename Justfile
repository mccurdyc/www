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
export FASTLY_SERVICE_ID := `op item get Fastly --fields service_id --reveal`
export FASTLY_API_KEY := `op item get Fastly --fields purge_token --reveal`

set quiet := false

shebang := "/usr/bin/env bash"

default: deploy

serve:
    hugo serve --baseURL http://nuc:1313 --bind 0.0.0.0

build:
    hugo --ignoreCache

deploy: build
    ./scripts/deploy.sh

rename-seq dir: clean-images
    ./scripts/rename-seq.sh "/mnt/photos/{{ dir }}"

# Usage - just sync-images '2024/early'
sync-images dir:
    just rename-seq {{ dir }}
    gsutil -m rsync -d -r "/mnt/photos/{{ dir }}/" "gs://images.mccurdyc.dev/images/{{ dir }}/"

# Usage - just dump-images '2024/early'
dump-images dir:
    ./scripts/dump-images.sh {{ dir }}

# Remove _L***.jpg images
clean-images:
    find /mnt/photos -name "._*" -exec sudo rm -rf {} \;

# Uploads book cover images to GCS
sync-bookcovers:
    gsutil -m rsync -d -r "/mnt/photos/book-covers" "gs://images.mccurdyc.dev/images/book-covers"

# List images
list-images dir:
    gsutil ls gs://images.mccurdyc.dev/images/{{ dir }}
