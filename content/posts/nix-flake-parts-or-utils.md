---
title: "Nix `flake-parts`, `flake-utils` or neither?"
description: ""
author: ""
date: 2026-02-01T09:24:46-05:00
subtitle: ""
image: ""
post-tags: []
posts: []
draft: false
---

NOTE: Frankly, I'm not in love with flakes. I think what flakes provide is extremely valuable, but I don't think I agree
with the implementation. Go read - https://determinate.systems/blog/nix-flakes-explained/

Again, my biggest complaint with Nix are the abstractions. I think many introduce too much indirection and make it
hard to understand what's going on. I understand that this is _a_ goal of abstractions. I think abstractions can either
be "heavy" or "light", where you don't need to know anything or you still need to be aware and the abstraction is there
to make it nicer, respectively. [`devenv`](https://devenv.sh) is a good example of a "heavy" abstraction. With something
so core to my day-to-day, I often want "light" abstractions so that I can still remain aware of how things work. Therefore,
I opt to not use `devenv`. Between raw flakes and `devenv` there are a few options --- ranging from minimal to "heavier":
`nixpkgs.lib.systems.flakeSystems`, `flake-utils` and `flake-parts`.

Honestly, I started this post thinking that I wanted to move away from `flake-parts` to something simpler like `flake-utils`,
but ended up preferring the module system of `flake-parts`. Use `flake-parts` if you plan to pull pieces of your flake into
re-usable modules, otherwise, it's likely unnecessary.

## `nixpkgs.lib.systems.flakeSystems` - standard Nixpkgs library functions

Honestly, I like this approach quite a bit. Just a bit of redundancy, but it's clear.

```nix
{
    description = "foo";
    inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    outputs = { self, nixpkgs }: let
        systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
        forAllSystems = nixpkgs.lib.genAttrs systems;
    in {
        packages = forAllSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        in {
        default = pkgs.hello;
        my-tool = pkgs.cowsay;
        });

        devShells = forAllSystems (system: let
        pkgs = nixpkgs.legacyPackages.${system};
        in {
            default = pkgs.mkShell {
                packages = with pkgs; [ gcc git ];
            };
        });
    }
}
```

## flake-utils - light abstraction to manage `system` nicer

It feels like a nice abstraction to remove the redundancy.

```nix
{
description = "foo";

inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
inputs.flake-utils.url = "github:numtide/flake-utils";

outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
    pkgs = nixpkgs.legacyPackages.${system};
    in {
        packages = {
            default = pkgs.hello;
            my-tool = pkgs.cowsay;
        };

        devShells.default = pkgs.mkShell {
            packages = with pkgs; [ gcc git ];
        };
    });
}
```

## flake-parts - Re-usable Modules

See my playground project where I was learning `flake-parts` - https://github.com/mccurdyc/playground/tree/main/nix/flake-parts)

```nix
{
description = "foo";

inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
inputs.flake-parts.url = "github:hercules-ci/flake-parts";

outputs = { flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit self; } {
        perSystem = { pkgs, ... }: {
            packages = {
                default = pkgs.hello;
                my-tool = pkgs.cowsay;
            };

            devShells.default = pkgs.mkShell {
                packages = with pkgs; [ gcc git ];
            };
        };
    };
}
```

flake-parts: A framework to configure flakes via nix modules

Write Nix modules --- exposing `options` to configure `config` --- which are consumed in a top-level
flake using flake-parts. flake-parts evaluates `import`ed modules and sets `self'`.

### Nix Modules: returns a configured `config` attrset

Before we try to understand flake-parts, we must understand the inner-workings of modules.

[The magic of modules is defined in `evalModules`](https://github.com/NixOS/nixpkgs/blob/2b10a50ae3da5b008025eefa9a440d95559bccde/lib/modules.nix#L84) i.e., the merging of `options` into `config`.

`<nixpkgs>.lib.evalModules` - https://nixos.org/manual/nixpkgs/stable/#module-system-lib-evalModules

In short, `evalModules` relies heavily on the laziness of Nix evaluations as well as a complex merging algorithm that defines
mergable types and priorities. The merging reminded me a bit of Cue at first where we are ultimately normalizing to a single
"flat" object that has `options` and `configs` fields. However, Cue is much stricter and prevents "overrides" where Nix
differs in that it defines an algorithm to handle them.

### flake-parts: A framework to configure flakes via nix modules

Defines a reusable module-sharing pattern, similar to `nixosModules` or `darwinModules`. These modules
are primarily used to define and configure options on a per-system basis, then to be consumed as proper
flake attributes.

This is allowed because there is nothing inherently in nix flakes that validate the output schema.

You can define arbitrary extra fields. `flakeModules` is the established "arbitrary field" used by
flake-parts. Then, it's on the consumer to actually consume these `flakeModules` in such a way that
actually makes sense, such as using it for `devShells` or something.

flake-parts is just a module system evaluator that:

1. Takes modules (with arbitrary options)
2. Evaluates them (merging configs, type-checking, etc.)
3. Returns an attrset

It doesn't care what the options are named - devShells, packages, mccurdyc-rust, banana - all the same to flake-parts.

#### `flake-module.nix`: _The_ nix module to configure a flake.

A nix module that defines flake or per-system -level flake attributes?

##### `providerInputs`

This prevents consuming flakes from having to explicitly define inputs when instead I could define inputs within the providing flake.

