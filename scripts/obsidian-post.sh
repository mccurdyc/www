#!/usr/bin/env bash
set -euo pipefail

VAULT_DIR="${HOME}/src/github.com/mccurdyc/obsidian.md"
POSTS_DIR="$(cd "$(dirname "$0")/.." && pwd)/content/posts"

slugify() {
  local input="$1"
  printf '%s' "$input" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9]/-/g' \
    | tr -s '-' \
    | sed 's/^-//;s/-$//'
}

mkdir -p "$POSTS_DIR"
cd "$VAULT_DIR"

mapfile -t public_notes < <(zk list --tag public --format path -q)

if [ ${#public_notes[@]} -eq 0 ]; then
  echo "No public notes found."
  exit 0
fi

copied=0
for rel_path in "${public_notes[@]}"; do
  source_file="${VAULT_DIR}/${rel_path}"
  if [ ! -f "$source_file" ]; then
    echo "Warning: missing file ${source_file}" >&2
    continue
  fi

  # Drop the .md extension, slugify the full vault-relative path, re-add .md.
  base_no_ext="${rel_path%.md}"
  slug="$(slugify "$base_no_ext").md"
  dest_file="${POSTS_DIR}/${slug}"

  cp "$source_file" "$dest_file"
  echo "${rel_path} -> ${dest_file}"
  copied=$((copied + 1))
done

echo "Copied ${copied} note(s) to ${POSTS_DIR}"
