default: help

.PHONY: serve
serve: ## Serves the statically-generated site locally.
	hugo serve

.PHONY: build
build: ## Re-compiles the static assets.
	hugo --ignoreCache

.PHONY: deploy
deploy: build ## Deploys the changes to the GCS bucket.
	export FASTLY_SERVICE_ID="$$(op get item Fastly --fields service_id)"; \
	export FASTLY_API_KEY="$$(op get item Fastly --fields api_key)"; \
	./scripts/deploy.sh

.PHONY: help
help: ## Prints this help menu.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
