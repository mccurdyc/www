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
	export FASTLY_API_KEY="$$(op item get Fastly --fields purge_token)"; \
	./scripts/deploy.sh

.PHONY: rename-seq
rename-seq: clean-images ## Renames images to sequential ordering
	./scripts/rename-seq.sh "/mnt/photos/$(DIR)"

.PHONY: sync-images
sync-images: ## Uploads images to GCS
	@# Usage - "make sync-images DIR='2024/early'"
	@$(MAKE) rename-seq DIR="$(DIR)"
	gsutil -m rsync -d -r "/mnt/photos/$(DIR)/" "gs://images.mccurdyc.dev/images/$(DIR)/"

.PHONY: dump-images
dump-images: 
	@# Usage - "make dump-images DIR='2024/early'"
	@./scripts/dump-images.sh "$(DIR)"

.PHONY: clean-images
clean-images: ## Remove _L***.jpg images
	find /mnt/photos -name "._*" -exec sudo rm -rf {} \;

.PHONY: sync-bookcovers
sync-bookcovers: ## Uploads book cover images to GCS
	gsutil -m rsync -d -r "/mnt/photos/book-covers" "gs://images.mccurdyc.dev/images/book-covers"

.PHONY: list-images
list-images: ## List images
	gsutil ls gs://images.mccurdyc.dev/images/$(DIR)

.PHONY: help
help: ## Prints this help menu.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
