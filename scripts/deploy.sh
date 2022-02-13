#!/bin/bash

set -ux -o pipefail

function main() {

  # Delete all remote files
  gsutil -m rm -r gs://www.mccurdyc.dev/**

  # Make sure that only items that were clean-built get deployed; nothing stale or cached.
  rm -rf public
  hugo --ignoreCache

  # Deploy!
  # Make sure to set the gcloud account using: gcloud auth application-default login
  hugo deploy --force --maxDeletes -1
gsutil -m rsync -r gs://images.mccurdyc.dev/images gs://www.mccurdyc.dev/images

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

main
