#!/usr/bin/env bash

set -ux -o pipefail

function main() {
	# Build site!
	rm -rf public
	hugo --ignoreCache --buildFuture --enableGitInfo

	# Deploy!
	# Make sure to set the gcloud account using: gcloud auth application-default login
	hugo deploy --force --maxDeletes -1
	# Make sure images are synced after deploy
	gsutil -q -m rsync -r gs://images.mccurdyc.dev/images gs://www.mccurdyc.dev/images
  # https://docs.fastly.com/en/guides/controlling-caching
	gsutil -q -m setmeta -r -h "Cache-Control: no-store, max-age=0, s-maxage=31557600" gs://www.mccurdyc.dev/*

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
