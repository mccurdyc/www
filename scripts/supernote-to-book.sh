#!/usr/bin/env bash
set -euo pipefail

SUPERNOTE_DIR="$HOME/src/github.com/mccurdyc/obsidian.md/SuperNote"
BOOKS_DIR="$(cd "$(dirname "$0")/.." && pwd)/content/books"
TZ_OFFSET="$(date +%:z)"

slugify() {
  local title="$1"
  # Replace '_ ' with ' ' (remove underscore artifacts)
  title="${title//_ / }"
  echo "$title" \
    | tr '[:upper:]' '[:lower:]' \
    | sed 's/[^a-z0-9 ]/ /g' \
    | tr -s ' ' '-' \
    | sed 's/^-//;s/-$//'
}

display_title() {
  local title="$1"
  # Replace '_ ' with ': ' to restore colons
  echo "${title//_ /: }"
}

parse_authors() {
  local raw="$1"
  # Strip [[ and ]]
  raw="${raw#\[\[}"
  raw="${raw%\]\]}"
  # Split on '; ' and format as YAML array
  local result="["
  local first=true
  while IFS= read -r author; do
    author="$(echo "$author" | sed 's/^ *//;s/ *$//')"
    [ -z "$author" ] && continue
    if [ "$first" = true ]; then
      first=false
    else
      result+=", "
    fi
    result+="\"$author\""
  done <<< "$(echo "$raw" | tr ';' '\n')"
  result+="]"
  echo "$result"
}

mkdir -p "$BOOKS_DIR"

highlights_tmp="$(mktemp)"
trap 'rm -f "$highlights_tmp"' EXIT

for file in "$SUPERNOTE_DIR"/*.md; do
  [ -f "$file" ] || continue

  full_title=""
  author_raw=""
  year=""
  read_date=""

  # Parse metadata
  in_metadata=false
  in_highlights=false
  true > "$highlights_tmp"

  while IFS= read -r line; do
    if [[ "$line" == "## Metadata" ]]; then
      in_metadata=true
      in_highlights=false
      continue
    fi
    if [[ "$line" == "## Highlights" ]]; then
      in_metadata=false
      in_highlights=true
      continue
    fi

    if $in_metadata; then
      case "$line" in
        "- Full Title: "*)
          full_title="${line#- Full Title: }"
          ;;
        "- Author: "*)
          author_raw="${line#- Author: }"
          ;;
        "- Year: "*)
          year="${line#- Year: }"
          ;;
        "- Read Date: "*)
          read_date="${line#- Read Date: }"
          ;;
      esac
    fi

    if $in_highlights; then
      if [[ "$line" =~ ^-\ .+\(Page\ ([0-9]+),\ Chapter\ ([0-9]+)\)$ ]]; then
        page="${BASH_REMATCH[1]}"
        chapter="${BASH_REMATCH[2]}"
        # Strip leading "- " and trailing "(Page X, Chapter Y)"
        text="$line"
        text="${text#- }"
        text="${text% \(Page *}"
        printf '%04d\t%04d\t%s\n' \
          "$chapter" "$page" "$text" \
          >> "$highlights_tmp"
      fi
    fi
  done < "$file"

  [ -z "$full_title" ] && continue

  disp_title="$(display_title "$full_title")"
  slug="$(slugify "$full_title")"
  authors="$(parse_authors "$author_raw")"
  out_file="$BOOKS_DIR/${slug}.md"

  # Build book-tags
  book_tags='["book"'
  if [ -n "$year" ]; then
    book_tags+=", \"$year\""
  fi
  book_tags+=']'

  # Use Read Date if available, otherwise current date
  if [ -n "$read_date" ]; then
    post_date="${read_date}T00:00:00${TZ_OFFSET}"
  else
    post_date="$(date +%Y-%m-%dT%H:%M:%S%:z)"
  fi

  # Write frontmatter
  cat > "$out_file" <<EOF
---
title: "$disp_title"
subtitle: ""
description: ""
author: "Colton J. McCurdy"
date: $post_date
image: "/image/book-covers/$slug/cover.jpg"
book-tags: $book_tags
books: ["$disp_title"]
book-authors: $authors
amazon: ""
thriftbooks: ""
draft: false
---
EOF

  # Write highlights grouped by chapter, sorted
  sort -t$'\t' -k1,1n -k2,2n "$highlights_tmp" \
    | awk -F'\t' '
    BEGIN { prev_ch = "" }
    {
      ch = $1 + 0
      page = $2 + 0
      text = $3
      if (ch != prev_ch) {
        if (prev_ch != "") printf "\n"
        printf "\n## Chapter %d\n\n", ch
        prev_ch = ch
      } else {
        printf "\n"
      }
      printf "p%d - %s\n", page, text
    }
  ' >> "$out_file"

  echo "Created: $out_file"
done
