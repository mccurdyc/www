#!/usr/bin/env bash

set -ux -o pipefail

while read -r source dest
do
  tmpfile=$(mktemp)
  destdir="/mnt/photos/book-covers/$dest"
  mkdir -p "$destdir"

  wget -O "$tmpfile" "$source"
  mv "$tmpfile" "$destdir/cover.jpg"
done < "$(dirname $0)/data/covers.csv"
