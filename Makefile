default: help

.PHONY: serve
serve: ## Serves the statically-generated site locally.
	hugo serve

.PHONY: build
build: ## Re-compiles the static assets.
	hugo --ignoreCache

.PHONY: deploy
deploy: build ## Deploys the changes to the GCS bucket.
	export FASTLY_SERVICE_ID="$$(op item get Fastly --fields service_id)"; \
	export FASTLY_API_KEY="$$(op item get Fastly --fields api_key)"; \
	./scripts/deploy.sh

.PHONY: sync-images
sync-images-%: ## Uploads images to GCS
	gsutil -m rsync -r /mnt/photos/$* gs://images.mccurdyc.dev/images/$*

.PHONY: sync-bookcovers
sync-bookcovers: ## Uploads book cover images to GCS
	$(MAKE) sync-images-book-covers

.PHONY: help
help: ## Prints this help menu.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
