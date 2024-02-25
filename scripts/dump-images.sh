#!/usr/bin/env bash

gsutil ls "gs://images.mccurdyc.dev/images/$1" | sed -En 's/gs:\/\/images.mccurdyc.dev(.*)$/{{< figure src="\1" >}}/p'
