---
title: "NixOS Config"
description: "Setting up my first NixOS system."
author: ""
date: 2022-09-04T21:35:06-04:00
subtitle: ""
image: ""
post-tags: ["linux", "nixos", "personal setup"]
posts: ["NixOS Config"]
draft: false
hide: false
---

# Context

I have a headless server (an Intel NUC). I am migrating [from an Arch Linux machine](https://www.mccurdyc.dev/posts/2020/03/my-arch-linux-install-and-configuration-on-a-dell-xps-13-7390-2019/)
to NixOS. These steps are not intended to be followed by anyone other than myself,
however, I've tried to add context to explain what I'm doing.

## Key Decisions

1. I don't plan to encrypt my drive.

Primarily so that if I have a power blip at home while I'm away, I don't have to
worry about not being able to decrypt the drive on startup in order to be able
to login remotely.

 believe there are ways to be able to decrypt the drive automatically on startup
 if a ubikey or USB is plugged in, but I haven't looked too deeply and I need
 to get my machine working immediately. This is something I can revisit later.

2. I wanted a repository / project structure that would allow for setting some
shared configuration across machines, architectures, users, etc. and would
allow overrides.

These projects where the ones I referred to most during my setup:

- [kclejeune/system](https://github.com/kclejeune/system)
- [notusknot/dotfiles-nix](https://github.com/notusknot/dotfiles-nix)
- [mitchellh/nixos-config](https://github.com/mitchellh/nixos-config)

You might find others that you like [here](https://nixos.wiki/wiki/Configuration_Collection).

I wanted to have a base "headless" config and then a GUI config for other machines.

## Personal Takeaways

I love the "feel" of running `nixos-rebuild switch` and things just working.
I would say, in general though, things still feel a bit early --- even though Nix
and NixOS is not new; Flakes are still experimental meaning APIs could change,
documentation and examples have some gaps and there seems to be a serious lack
of clear standards in terms of project structure.

# Guide

## Preparing a bootable USB

<https://nixos.org/guides/building-bootable-iso-image.html>

1. Re-partition the USB just to wipe it.

  ```
  sudo fdisk /dev/sda
  (fdisk): g
  (fdisk): n (skip, skip, +512M)
  (fdisk): t (1)
  (fdisk): n (skip, skip, skip)
  (fdisk): w
  ```

2. Check the partitions

  ```
  sudo parted /dev/sda print
  ```

3. Reformat the USB

  ```
  sudo mkfs.fat -F32 -nESP /dev/sda1
  sudo mkfs.ext4 /dev/sda2
  ```

4. Load the NixOS iso onto the USB

  ```
  sudo dd bs=4M if=/home/mccurdyc/Downloads/nixos-minimal-22.05.2485.3d47bbaa26e-x86_64-linux.iso of=/dev/sda status=progress
  sync
  ```

## Partitioning Target Machine

1. Check out what drives we have.

  ```
  lsblk
  ```

2. Partition drives.

I'm going to make a boot and root partition. In the past, I had a separate
root (25G) and home partition and ran into many issues with tools like Docker
(easily fixable by changing image location) and Arch's package manager filling
up the root partition.

  ```
  sudo fdisk /dev/nvme0n1
  (fdisk): g
  (fdisk): n (skip, skip, +512M)
  (fdisk): t (1)
  (fdisk): n (skip, skip, skip)
  (fdisk): w
  ```

3. Check the partitions

  ```
  sudo parted /dev/nvme0n1 print
  ```

4. Reformat the target drives

  ```
  sudo mkfs.fat -F32 -nESP /dev/nvme0n1p1
  sudo fatlabel /dev/nvme0n1p1 NIXBOOT
  sudo mkfs.ext4 /dev/nvme0n1p2 -L NIXROOT
  ```

5. Mount the target drives

<https://nixos.wiki/wiki/NixOS_Installation_Guide>

  ```
  sudo mount /dev/disk/by-label/NIXROOT /mnt
  sudo mkdir -p /mnt/boot
  sudo mount /dev/disk/by-label/NIXBOOT /mnt/boot
  ```

6. Generate the NixOS configuration on the target filesystem!!!

<https://nixos.wiki/wiki/NixOS_Installation_Guide>

  ```
  sudo nixos-generate-config --root /mnt
  ```

7. Tweak the configuration.

- [/mnt/etc/nixos/configuration.nix](https://github.com/mccurdyc/nixos-config/blob/40d8d7828d4902d43a9aaf7b1a7f3ac7a7a9a673/nixos/configuration.nix)
- [/mnt/etc/nixos/hardware-configuration.nix](https://github.com/mccurdyc/nixos-config/blob/40d8d7828d4902d43a9aaf7b1a7f3ac7a7a9a673/nixos/hardware-configuration.nix)

8. NixOS install

  ```
  cd /mnt
  sudo nixos-install
  ```

## NixOS

### Building a New Generation

<https://nixos.wiki/wiki/Overview_of_the_NixOS_Linux_distribution#Generations>

1. Build

  ```
  sudo nixos-rebuild build
  sudo nixos-rebuild switch
  sudo nixos-rebuild switch --flake '.#intel' # flakes
  ```

I love this command!! It just feels so good! It feels immutible.

2. Rollbacks

```
nix-env --rollback               # roll back a user environment
nixos-rebuild switch --rollback  # roll back a system environment
```

## Home Manager

<https://nixos.wiki/wiki/Home_Manager>
<https://nix-community.github.io/home-manager/index.html>
<https://nix-community.github.io/home-manager/options.html>

1. Install home-manager

  ```
  sudo nix-channel --add https://github.com/nix-community/home-manager/archive/release-22.05.tar.gz home-manager
  sudo nix-channel --add https://nixos.org/channels/nixos-22.05 nixos
  sudo nix-channel --update
  ```

2. Create file

  ```
  sudo nix-shell '<home-manager>' -A install
  ```

  ```
  # /home/mccurdyc/.config/nixpkgs/home.nix
  ```

3. Make a change; run

  ```
  home-manager build
  home-manager switch
  ```

4. After migrating to Flakes, I no longer have to manage this separately.

  ```
  sudo nixos-rebuild switch --flake '.#intel'
  ```

# References / Notes

## Formatters for Nix lang

- <https://github.com/nix-community/nixpkgs-fmt>
- <https://github.com/kamadorueda/alejandra>
  - <https://github.com/kamadorueda/alejandra/blob/main/STYLE.md>

If I did this all again, I would have setup a formatter first so that rebasing
commits after would be easier. It probably wouldn't have made a huge difference
because I ended up just editing the files during the rebase anyway.

I ended up choosing `alejandra` as my formatter of choice, but may end up switching
to `nixpkgs-fmt` because the experimental Nix LSP client `[rnix-lsp](https://github.com/nix-community/rnix-lsp)`
uses `nixpkgs-fmt`.

## Flakes

<https://nixos.wiki/wiki/Flakes>

- still in beta phase
- Flakes allow you to specify your code's dependencies (e.g. remote Git repositories)
in a declarative way
- Enabling Flakes

  ```
  # /etc/nixos/configuration.nix
  nix.settings.experimental-features = [ "nix-command" "flakes" ];
  ```

- With the help from @phamann, I was able to setup my Flake to manage my Vim plugins
[in this commit](https://github.com/mccurdyc/nixos-config/commit/98bfdc1589a5f9adbe26a25e70930b86bf8229ed).

## <https://www.tweag.io/blog/2020-05-25-flakes/>

- Note that any file that is not tracked by Git is invisible during Nix evaluation,
in order to ensure hermetic evaluation.
  - I really liked this aspect.
- The `inputs` attribute specifies other flakes that this flake depends on. These
are fetched by Nix and passed as arguments to the `outputs` function.
- The `outputs` attribute is the heart of the flake: it’s a function that produces
an attribute set.
- The `self` argument denote _this_ flake. Its primarily useful for referring to
the source of the flake (as in `src = self;`) or to other outputs
(e.g. `self.defaultPackage.x86_64-linux`)
- The attributes produced by `outputs` are arbitrary values, except that (as we
saw above) there are some standard outputs such as `defaultPackage.${system}`.
- `nixos-rebuild switch --flake /path/to/my-flake#my-machine` builds and activates
the configuration specified by the flake output `nixosConfigurations.my-machine`.
If you omit the name of the configuration (`#my-machine`), `nixos-rebuild` defaults
to using the current host name.

## <https://www.tweag.io/blog/2020-07-31-nixos-flakes/>

- NixOS is currently built around a _monorepo_ workflow — the entire universe
should be added to the `nixpkgs` repository, because anything that isn’t, is much
harder to use.
- `nix flake show templates`

  ```
  # nix flake show templates
  github:NixOS/templates/2f86534428917d96d414964c69a5cfe353500ad5
  ├───defaultTemplate: template: A very basic flake
  └───templates
      ├───bash-hello: template: An over-engineered Hello World in bash
      ├───c-hello: template: An over-engineered Hello World in C
      ├───compat: template: A default.nix and shell.nix for backward compatibility with Nix installations that don't support flakes
      ├───full: template: A template that shows all standard flake outputs
      ├───go-hello: template: A simple Go package
      ├───haskell-hello: template: A Hello World in Haskell with one dependency
      ├───hercules-ci: template: An example for Hercules-CI, containing only the necessary attributes for adding to your project.
      ├───pandoc-xelatex: template: A report built with Pandoc, XeLaTex and a custom font
      ├───python: template: Python template, using poetry2nix
      ├───rust: template: Rust template, using Naersk
      ├───rust-web-server: template: A Rust web server including a NixOS module
      ├───simpleContainer: template: A NixOS container running apache-httpd
      └───trivial: template: A very basic flake
  ```

- `nix flake init -t templates#simpleContainer`
- Nixpkgs overlays add or override packages in the `pkgs` set.

### direnv + nix-shell

[In this commit](https://github.com/mccurdyc/nixos-config/commit/2504d7f927df83a49912584ee48852802b1eba83),
I started using `direnv` and defined a `flakify` shell function for easily adding
direnv config with Flake support to repos.

[Here](https://github.com/mccurdyc/www/commit/0d7aa6b627a380d0123388de3a8f84c92f142ce5)
is an example use of `nix-direnv` with a Flake for my website repo which has `gcloud`
and `hugo` as build dependencies.

- <https://scrive.github.io/nix-workshop/02-nix-commands/02-use-packages-in-nix-shell.html>
- <https://github.com/direnv/direnv/wiki/Nix>
- <https://direnv.net/man/direnv-stdlib.1.html> hooks mentioned by Zeke

## Home Manager `programs.${program}` Configuration Steps

<https://nix-community.github.io/home-manager/options.html>

- Tailscale

  - <https://fzakaria.com/2020/09/17/tailscale-is-magic-even-more-so-with-nixos.html>
  - [In this commit](https://github.com/mccurdyc/nixos-config/commit/8b60f71f7324365fb72a09fb6b487164aec675ed),
  I updated my system Tailscale package to use the `unstable` channel so that I
  could use the latest version of Tailscale as it comes available.

- git

  - gpg key import
  - Ran into issues importing my gpg key
  - <https://github.com/NixOS/nixpkgs/issues/35464>
    - `gpgconf --reload gpg-agent` fixed it

- NeoVim

  - **NOTE: there doesn't seem to be and official, fully-supported way to generate
  an `init.lua` instead of `init.vim` in NixOS.**
  - I was looking at <https://github.com/nix-community/home-manager/blob/b382b59faf717c5b36f4cd8e1c5d96cdabd382c9/modules/programs/neovim.nix#L200>
  but it's a readonly value and I'd get the following error:

    ```
    error: The option `home-manager.users.mccurdyc.programs.neovim.generatedConfigs' is read-only, but it's set multiple times.
    ```

  - <https://nixos.wiki/wiki/Neovim#Note_on_errors_using_default_.60packages.60_for_plugins_requiring_Lua_modules>
  - <https://github.com/nix-community/home-manager/issues/1907>
  - <https://www.youtube.com/watch?v=rUvjkBuKua4>
  - <https://github.com/nix-community/home-manager/issues/1907#issuecomment-887573079>
  - <https://github.com/mtrsk/nixos-config/blob/6221ef7625ca1f8d72321a13ab800429ea59e977/home/editors.nix#L25>
  - <https://github.com/notusknot/dotfiles-nix>
  - <https://github.com/nix-community/rnix-lsp>
  - diffview and coq_nvim ended up causing issues with how they were being loaded into init.vim
  - readonly filesystem issues
  - `:GoUpdateBinaries` fails
  - `:COQdeps fails`
    - I needed to update my config directory.
  - <https://github.com/NixOS/nixpkgs/issues/168928#issuecomment-1109581739>
  - I had a weird bug with the title bar
    - `set notitle` fixed it

## Headed Server

  (Haven't got here yet. This part of the post will be updated once I get here.)

- firefox
- feh
- alacritty
- i3-status
  - <https://github.com/greshake/i3status-rust>
- rofi
- zathura
- picom
- polybar
- spotifyd
- status-notifier-watcher
- xsession
  - i3
- xresources

## Other Thing to Look Into

- <https://github.com/divnix/digga>
  - <https://github.com/divnix/digga/tree/main/examples/devos>
  - <https://github.com/montchr/dotfield/tree/main/home/profiles>

## General References

- <http://ryantm.github.io/nixpkgs/using/configuration/>
- <https://nixos.org/guides/nix-pills/basics-of-language.html#idm140737320575616>
