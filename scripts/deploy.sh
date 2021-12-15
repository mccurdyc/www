#!/bin/bash

set -ux -o pipefail

function main() {
  # Copy .well-known from remote since it's not managed by Hugo and gets deleted.
  mkdir -p .well-known
  gsutil -m cp -r gs://www.mccurdyc.dev/.well-known/* .well-known

  # Delete all remote files
  gsutil -m rm -r gs://www.mccurdyc.dev/**

  # Make sure that only items that were clean-built get deployed; nothing stale or cached.
  rm -rf public
  hugo --ignoreCache

  # Deploy!
  # Make sure to set the gcloud account using: gcloud auth application-default login
  hugo deploy --force --maxDeletes -1

  # Push .well-known back up to remote for Fastly TLS validation.
  gsutil cp -r .well-known gs://www.mccurdyc.dev

  # Purge Fastly cache
  if [ -z "${FASTLY_SERVICE_ID}" ]; then
    echo "FASTLY_SERVICE_ID is not set."
    exit 1
  fi

  if [ -z "${FASTLY_API_KEY}" ]; then
    echo "FASTLY_API_KEY is not set."
    exit 1
  fi

  curl -X POST -H "Fastly-Key: ${FASTLY_API_KEY}" "https://api.fastly.com/service/${FASTLY_SERVICE_ID}/purge_all"
}

function gsutil() {
  docker run --rm -ti \
    -v "$HOME/.config/gcloud:/root/.config/gcloud" \
    -w "/root" \
    google/cloud-sdk gsutil "$@"
}

main
