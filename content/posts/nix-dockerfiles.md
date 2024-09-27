---
title: "Why I Avoid Using Nix to Build Docker Images"
description: "It's a useful tool; but it shouldn't be your default"
author: ""
date: 2024-09-11T08:22:14-04:00
subtitle: ""
image: ""
post-tags: ["nix", "2024"]
posts: []
draft: false
---

I personally haven't used Nix to build Docker images because I haven't needed to
prioritize long-term stability. I think it's a great tool to have available and I'm sure
I will eventually reach for it, but need has to outweigh the significant cost
of introducing Nix into the main development path. Generally, I think we must always
do a cost-benefit analysis.

I add Nix flakes to all of the projects that I work in. But NOT as part of the
main development workflow. I add flakes to projects so that other folks who have
already opted-IN to Nix can leverage the tooling. If you don't want to use Nix,
but want all of the dev tools for the project, I provide a Docker image that has
all of the tools installed.

Nix has an extremely high learning curve and unless the entire organization ---
even just the team opting-in is often NOT enough; teams change --- has opted-in to Nix
being part of the "golden path".

Dockerfiles are an amazing interface. Folks in the industry at this point are
familiar with them. The cost to use a Dockerfile is extremely low. Therefore,
introducing an extremely high-cost alternative needs to bring with it and extremely,
EXTREMELY high benefit.

```docker
# Reference(s)
# - https://mitchellh.com/writing/nix-with-dockerfiles
#
# Context / Motivation
# - I do NOT want to build a Docker image in Nix (unless I need hermetic builds).
#     - It's the wrong interface, generally speaking.
# - I got tired of pinning dependencies in two places in different ways
#
# https://hub.docker.com/r/nixos/nix/
FROM nix:latest AS base

RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

# Copy all nix files into the image
COPY flake.nix flake.lock /src/
COPY nix /src/nix # if you have other nix files that you reference

WORKDIR /src

# These are NOT used in CI because of how commands are passed to the container and hence
# why we have 'nix develop --comand ...' everywhere. This is for local use via
# 'docker run --rm --name nix --volume $(pwd):/src nix:latest <command>'
ENTRYPOINT [ "nix", "--extra-experimental-features", "nix-command flakes", "develop", "--command" ]
# Default command that can be overriden
CMD ["bash"]
```
