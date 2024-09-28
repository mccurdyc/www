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
ENTRYPOINT [ "nix", "develop", "--command" ]
# Default command that can be overriden
CMD ["bash"]
```

## But, that still bleeds Nix outside of the Dockerfile interface

You may ask, how?

1. You run `nix develop --command <...>` to execute commands.
1. You can't run `nix develop --command <...>` in parallel because each execution takes a lock over the Nix store.

    ```txt
    SQLite database '/root/.cache/nix/eval-cache-v5/<hash>.sqlite' is busy
    ```

Folks that don't want to learn Nix just to get the dev tools should NOT have to
debug these problems. If you FORCE Nix, people will get a bad taste.

```nix
{
  description = "Repo configuration";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-24.05";
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixos-unstable";
    pre-commit-hooks.url = "github:cachix/pre-commit-hooks.nix";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs = inputs@{ self, nixpkgs, nixpkgs-unstable, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; }
      {
        flake = { };

        systems = [
          "aarch64-darwin"
          "x86_64-darwin"
          "x86_64-linux"
        ];

        # This is needed for pkgs-unstable - https://github.com/hercules-ci/flake-parts/discussions/105
        imports = [ inputs.flake-parts.flakeModules.easyOverlay ];

        perSystem = { system, ... }:
          let
            pkgs = import inputs.nixpkgs {
              inherit system;
              config.allowUnfree = true;
            };
            pkgs-unstable = import inputs.nixpkgs-unstable {
              inherit system;
              config.allowUnfree = true;
            };


            # See - https://github.com/mccurdyc/nix-templates/blob/main/full/nix/github.nix
            pinned_cue = pkgs.callPackage (import ./nix/github.nix) {
              inherit system;
              org = "cue-lang";
              name = "cue";
              version = "v0.10.0";
              # 'nix-prefetch-url https://github.com/cue-lang/cue/releases/download/v0.10.0/cue_v0.10.0_darwin_arm64.tar.gz'
              # https://github.com/NixOS/nixpkgs/blob/54b4bb956f9891b872904abdb632cea85a033ff2/doc/build-helpers/fetchers.chapter.md#update-source-hash-with-the-fake-hash-method
              sha256 = {
                "x86_64-linux" = "1liz2gkd0zj72xbg0fynsrcz1rsdqdpfjsgqzwbzv54wyrv9qi4g";
                "aarch64-darwin" = "06k72afvxl0jfa97b8f2b9r7fb7889m0dcqgx2hl6bv8ifp5sbpp";
                "x86_64-darwin" = "13r3nlh8y06735cnzd7qsq1kb8hfc057g5r4yvwfi2jjhyysrmnd";
              }.${system};
            };

            ci_packages = {
              cue = pinned_cue;
              curl = pkgs.curl;
              jq = pkgs.jq;
              just = pkgs-unstable.just; # need just >1.33 for working-directory setting
              yq = pkgs.yq-go;
            };

            packages = (builtins.attrValues ci_packages) ++ [
              pkgs.statix
              pkgs.nixpkgs-fmt
              pkgs-unstable.nil

              # Linters
              pkgs.yamllint

              # Kubernetes
              pkgs.kubectl
              pkgs.kubernetes-helm
              pkgs.kubie
              pkgs.stern

              # Docker
              pkgs.dive
              pkgs.docker
              pkgs.dockerfile-language-server-nodejs
              pkgs.hadolint
            ];
          in
          {
            # This is needed for pkgs-unstable - https://github.com/hercules-ci/flake-parts/discussions/105
            overlayAttrs = { inherit pkgs-unstable; };

            formatter = pkgs.nixpkgs-fmt;

            # https://github.com/cachix/git-hooks.nix
            # 'nix flake check'
            checks = {
              pre-commit-check = inputs.pre-commit-hooks.lib.${system}.run {
                src = ./.;
                hooks = {
                  # Nix
                  deadnix.enable = true;
                  nixpkgs-fmt.enable = true;
                  statix.enable = true;

                  # Shell
                  shellcheck.enable = true;
                  shfmt = {
                    enable = true;
                    entry = "shfmt --simplify --indent 2";
                  };
                };
              };
            };

            packages = ci_packages;

            devShells.default = pkgs.mkShell {
              inherit (self.checks.${system}.pre-commit-check) shellHook;
              buildInputs = self.checks.${system}.pre-commit-check.enabledPackages;
              inherit packages;
            };
          };
      };
}
```

```dockerfile
# Reference(s)
# - https://mitchellh.com/writing/nix-with-dockerfiles
#
# Context / Motivation
# - I do NOT want to build a Docker image in Nix (unless I need hermetic builds).
#     - It's the wrong interface, generally speaking.
# - I got tired of pinning dependencies in two places in different ways
FROM nixos/nix:latest AS base

RUN echo "experimental-features = nix-command flakes" >> /etc/nix/nix.conf

# Copy all nix files into the image
COPY flake.nix flake.lock /src/
# See - https://github.com/mccurdyc/nix-templates/blob/main/full/nix/github.nix
COPY nix /src/nix

WORKDIR /src

# Fetch CI dependencies
# These are deliberately each independent layers so that when ONE changes, we dont
# rebuild all
#
# To identify/debug the correct source path, run `nix buid .#<pkg>` outside of the dockerfile
RUN nix build .#cue && cp -v result/bin/cue /usr/bin/cue
RUN nix build .#curl && cp -v result-bin/bin/curl /usr/bin/curl
RUN nix build .#jq && cp -v result-bin/bin/jq /usr/bin/jq
RUN nix build .#just  && cp -v result/bin/just /usr/bin/just
RUN nix build .#yq && cp -v result/bin/yq /usr/bin/yq

# Motivation for having a final image?
# - Running `nix develop` in CI takes too long (>2min)
#   - Dependencies can be baked into the image
# - `nix develop` prevents commands from being run in parallel
FROM alpine:3.20.3

COPY --from=base /usr/bin/* /usr/bin/
```

## FUTURE: using `nixpkgs.dockerTools.buildImage`

TODO

- https://nixos.org/manual/nixpkgs/stable/#sec-pkgs-dockerTools
- https://nix.dev/tutorials/nixos/building-and-running-docker-images.html
- https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/docker/examples.nix
