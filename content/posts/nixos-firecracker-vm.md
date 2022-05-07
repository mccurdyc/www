---
title: "NixOS Firecracker VM"
description: "I've been playing with Firecracker VMs for a bit now and have become my primary means for PoCing things. And I've been wanting to switch to NixOS, but haven't had the time to move my primary machine."
author: ""
date: 2022-05-07
subtitle: ""
image: ""
post-tags: ["2022", "linux"]
posts: ["NixOS in a Firecracker VM"]
draft: false
---

## Motivation for NixOS

- Reproducible builds!
- Declarative configurations.

## Motivation for Using Firecracker VMs

I've been playing with Firecracker VMs for a bit now and have become my primary
means for PoCing things. And I've been wanting to switch to NixOS, but haven't
had the time to move my primary machine."

I've been asked "why not Docker? why VMs?" and honestly I don't have a great
technical reason for the decision. It's mostly from a learning viewpoint that
I've made this decision.

## Steps

1. Run the following as a non-root user
2. `sh <(curl -L https://nixos.org/nix/install) --daemon`
3. `nix-channel --add https://nixos.org/channels/nixos-21.11 nixpkgs`
4. `nix-channel --update`
5. `nix-env -f '<nixpkgs>' -iA nixos-install-tools`
6. Generate nixos configs

  ```
  sudo `which nixos-generate-config` --root /mnt
  ```

  This will create the following:

  ```
  [foo@archlinux ~]$ ls /mnt/etc/nixos/
  configuration.nix           hardware-configuration.nix
  ```

7. Make some minimal tweaks to these generated files

  - Set the following in `/etc/nixos/configuration.nix`

  ```
  users.users.root.initialHashedPassword = "";
  boot.loader.grub.device = "nodev"; # or "nodev" for efi only
  networking.hostName = "nixos"; # Define your hostname.
  time.timeZone = "America/NewYork";
  environment.systemPackages = with pkgs; [
    vim
    wget
    firefox
  ];
  services.openssh.enable = true;
  ```

  - Added the following to `/etc/nixos/hardware-configuration.nix`
  ```
    fileSystems."/" = {
      device = "/dev/disk/by-uuid/<uuid>";
      fsType = "ext4";
    };
  ```

8. `sudo groupadd -g 30000 nixbld`
9. `sudo useradd -u 30000 -g nixbld -G nixbld nixbld`
10. `export NIX_PATH=/nix/var/nix/profiles/per-user/root/channels`

  ```
  [foo@archlinux ~]$ sudo PATH="$PATH" NIX_PATH="$NIX_PATH" `which nixos-install` --root /mnt
  building the configuration in /mnt/etc/nixos/configuration.nix...
  error: file 'nixpkgs/nixos' was not found in the Nix search path (add it using $NIX_PATH or -I)
  ```

  Found https://github.com/NixOS/nixpkgs/issues/149791#issuecomment-1107865859

11. Re-run `nixos-install`

  ```
  sudo PATH="$PATH" NIX_PATH="$NIX_PATH" `which nixos-install` --root /mnt
  ```

12. `sudo chown -R 0:0 /nix`
13. `for i in {1..32}; do sudo userdel -f nixbld${i}; done`
14. `sudo groupdel nixbld`
15. `pacman -S rsync`
16. **(on host)** `sudo mkdir /mnt/nixos-root && sudo rsync -a root@archlinux.localdomain:/mnt /mnt/nixos-root`
17. `[root@archlinux ~]# chroot /mnt/ /bin/sh` but there's nothing here except  `sh` and `env` which is expected from https://nixos.wiki/wiki/Nix_vs._Linux_Standard_Base
18.  Need to set my nix-profile in the chroot

  - https://nixos.org/manual/nix/stable/package-management/profiles.html
  - https://nixos.wiki/wiki/Change_root
