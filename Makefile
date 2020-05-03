default: help

.PHONY: serve
serve: ## Serves the statically-generated site locally.
	hugo serve

.PHONY: deploy
deploy: ## Deploys the changes to the GCS bucket.
	./scripts/deploy.sh

.PHONY: help
help: ## Prints this help menu.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
