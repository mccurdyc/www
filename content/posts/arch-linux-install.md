---
title: "Arch Linux Install on Dell XPS 13 7390 (2019)"
author: "Colton J. McCurdy"
type: ""
date: 2020-03-05
image: ""
tags: []
---

## Installing Arch on a USB

### USB Storage Arch

https://wiki.archlinux.org/index.php/USB_storage_devices
1. find the device with `lsblk -f`
2. `mkdir /mnt/usb`
3. `mount -U <UUID> /mnt/usb`
4. when done, `umount /mnt/usb`

### Grabbing and Arch `.iso`

1. Download the `*.iso` file from the [Arch Downloads page (HTTP Direct Downloads)](https://www.archlinux.org/download/)

### Creating bootable Arch image

http://valleycat.org/linux/arch-usb.html?i=1

`dd bs=4M if=$HOME/Downloads/archlinux.*.iso of=/dev/sda status=progress && sync`

### Plug the USB into the machine

1. while booting, keep smashing <F12>
2. Disabled Secure Boot and changed the boot order to have the USB first

Other BIOS stuff like changing SATA operating mode from `RAID` to `AHCI`
(this should now show your SSD when you boot arch)
https://github.com/nw2190/Arch_Install

## On the new machine

### Connect to wifi

1. make sure that the wireless drivers in the ISO were included and are supported

```bash
lspci -k | grep -A3 'Network controller'
```

2. `iw dev`
3. `ip link set wlan0 up`
4. `iw dev wlan0 scan | grep 'SSID:'`
5. `wpa_supplicant -i wlan0 -c <(wpa_passphrase 'McCurdyNetwork' 'password')`
> Once a connection is established, fork the process to the background by pressing [ctrl]+z and running `bg`.
6. lease an IP address with `dhcpcd wlan0`
7. Sync system time with `timedatectl set-ntp true`

### Partitioning

1. `lsblk` to get the USB device's name

followed steps here https://gilyes.com/Installing-Arch-Linux-with-LVM/

Specific details here
https://wiki.archlinux.org/index.php/installation_guide
and here https://wiki.archlinux.org/index.php/Partitioning#Example_layouts

UEFI/GPT layout

OLD
```bash
$ gdisk /dev/nvme0n1
$ d # (until all partitions are removed)
$ o
$ n # (skip, skip, +260M, ef00)
$ n # (skip, skip, +25G, 8304 <Linux x86-64 root (/)>)
$ n # (skip, skip, skip, 8302 <Linux /home>)
$ p (just to check)
$ w (write)
```

NEW

https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
$ fdisk /dev/nvme0n1
$ (fdisk) g
$ (fdisk) n (skip, skip, +512M)
$ (fdisk) t (1, 1)
$ (fdisk) n (skip, skip, skip)
```

I wanted to go this route, but my system would not allow Legacy boot mode (i.e., BIOS/MBR)

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

### Formatting the partitions

https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
# Should show "esp" in Flags:
$ parted /dev/nvme0n1 print

# Initialize it as FAT32
$ mkfs.fat -F32 -nESP /dev/nvme0n1p1

# Initialize the root filesystem
$ mkfs.ext4 /dev/nvme0n1p2
```

### Setup Encryption

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
# cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/nvme0n1p2
# cryptsetup luksOpen /dev/nvme0n1p2 luks
```

### LVM Partitions

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ pvcreate /dev/mapper/luks
$ vgcreate vg0 /dev/mapper/luks
$ lvcreate -L 8G vg0 -n swap
$ lvcreate -L 25G vg0 -n root
$ lvcreate -l 100%FREE vg0 -n home
```

### Format Partitions

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd
https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
$ mkfs.ext4 /dev/mapper/vg0-root
$ mkfs.ext4 /dev/mapper/vg0-home
$ mkswap /dev/mapper/vg0-swap
```

### Mount the filesystem

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ mount /dev/mapper/vg0-root /mnt
$ mkdir /mnt/{boot,home}
$ mount /dev/nvme0n1p1 /mnt/boot
$ mount /dev/mapper/vg0-home /mnt/home
$ swapon /dev/mapper/vg0-swap
```

### Install base packages that go with you to the root system

```bash
$ pacstrap -i /mnt base base-devel linux lvm2 linux-firmware nano iw dialog dhcpcd wpa_supplicant git vim openssh intel-ucode
```

### Generate `fstab`

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ genfstab -U /mnt >> /mnt/etc/fstab
```

### Enter the new system

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ arch-chroot /mnt /bin/bash
```

1. set timezone
```bash
# ln -s /usr/share/zoneinfo/America/US /etc/localtime
```

2. set locale

```bash
$ vim /etc/locale.gen (uncomment en_US.UTF-8 UTF-8)
$ locale-gen
$ echo LANG=en_US.UTF-8 > /etc/locale.conf
$ export LANG=en_US.UTF-8
```

3. set hardware clock

```bash
$ hwclock --systohc --utc
```

4. set hostname

https://wiki.archlinux.org/index.php/installation_guide

```bash
$ echo mccurdyc >/etc/hostname
```

`/etc/hosts`
```txt
127.0.0.1	localhost
::1		localhost
127.0.1.1	mccurdyc.localdomain	mccurdyc
```

5. create a user

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ useradd -m -g users -G wheel -s /bin/bash mccurdyc # the shells must be listed in $(cat /etc/shells) see - https://wiki.archlinux.org/index.php/users_and_groups
$ passwd mccurdyc
$ visudo # uncomment %wheel ALL=(ALL) ALL
```

6. Configure mkinitcpio with modules needed for the initrd image

```bash
$ vim /etc/mkinitcpio.conf
# Add 'encrypt' and 'lvm2' to HOOKS before 'filesystems'
$ mkinitcpio -p linux
```

7. setup the `systemd-boot` boot manager

`grub` isn't working on this laptop

https://www.cio.com/article/3098030/how-to-install-arch-linux-on-dell-xps-13-2016-in-7-steps.html
https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
# Make sure your ESP partition (described earlier) is mounted at /boot
$ mount -l | grep boot

$ bootctl --path=/boot install

# Get the UUID of your root partition
$ blkid -s UUID -o value /dev/nvme0n1p2

# create a `/boot/loader/entries/arch-encrypted-lvm.conf` file
$ vim /boot/loader/entries/arch-encrypted-lvm.conf
```

With the following

```
title Arch Linux Encrypted LVM
linux /vmlinuz-linux
initrd /intel-ucode.img
initrd /initramfs-linux.img
options cryptdevice=UUID=<UUID>:MyVol root=/dev/mapper/MyVol-root quiet rw
```

### Reboot

1. Leave chroot with `exit`
2. `reboot`

## After rebooting

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ systemctl enable dhcpcd.service
$ systemctl start dhcpcd.service
```

### Reconnect to the wifi

```bash
$ iw dev # the device name probably changed
$ sudo ip link set wlp2s0 up

# https://unix.stackexchange.com/questions/279545/failed-to-open-config-file-dev-fd-63-error-no-such-file-or-directory-for-wp
$ sudo su -c 'wpa_supplicant -i wlp2s0 -c <(wpa_passphrase "McCurdyNetwork" "password")'
```

### Install some necessary packages

https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ pacman -S networkmanager iw wpa_supplicant dialog wireless_tools base-devel xclip rofi alacritty
$ systemctl enable NetworkManager.service
$ systemctl enable wpa_supplicant.service
```

### Clone some helpful git repos

Install `yay` (my favorite AUR package manager, written in Go!)

```bash
$ git clone https://github.com/mccurdyc/dotfiles.git # ssh isn't configured yet
$ mkdir /home/mccurdyc/tools
$ git clone https://aur.archlinux.org/yay.git /home/mccurdyc/tools/yay
$ cd /home/mccurdyc/tools/yay
$ makepkg -si
```

### Install i3 Window Manager

```bash
$ sudo pacman -S xorg xorg-xclock xorg-twm xorg-xinit xterm i3 zsh tmux adobe-source-code-pro-fonts
$ echo "exec i3" >> ~/.xinitrc
$ startx
```

### Install Video drivers

https://wiki.archlinux.org/index.php/Intel_graphics

```bash
$ pacman -S vulkan-intel vulkan-mesa-layer # xf86-video-intel caused it to be super super laggy!!!
```

Make sure that `xf86-video-intel` is not installed. If your video is super laggy, it probably is installed.

### Install drivers (should fix ability to change screen brightness)

https://www.archlinux.org/groups/x86_64/xorg-drivers/

```bash
$ pacman -S xorg-drivers
```

### Setup ssh for `git clone`

https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

### Install Desktop Environment

### Install Display Manager (or login manager)

https://wiki.archlinux.org/index.php/Display_manager

> A display manager, or login manager, is typically a graphical user interface that is displayed at the end of the boot process in place of the default shell.

https://wiki.archlinux.org/index.php/CDM

```bash
$ yay -S cdm-git
```

### Other installs

```bash
$ yay -S brave-bin neovim
```

```bash
# https://aur.archlinux.org/packages/1password-cli/#pinned-652863
$ gpg --recv-keys 3FEF9748469ADBE15DA7CA80AC2D62742012EA22
$ yay -S 1password-cli

To list AUR packages on another machine, run `pacman -Qm`
