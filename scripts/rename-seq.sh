#!/usr/bin/env bash

set -ux -o pipefail

function main() {
  a=1
  for i in $1/*; do
    new=$(printf "$1/%04d.jpg" "$a")
    sudo mv -i -- "$i" "$new"
    let a=a+1
  done
}

main $1
