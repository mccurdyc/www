---
title: "My Arch Linux Install and Configuration on a Dell XPS 13 7390 (2019)"
author: "Colton J. McCurdy"
type: ""
date: 2020-03-05
image: ""
tags: ["arch", "2020", "linux"]
---

## Background

This post is rather selfish in nature and often does not describe what each command does.
It is not meant to be a post that "just works" for anyone, but rather so that others
can see how I installed Arch Linux on my machine (i.e., I use my device names, etc.).
Also, I am far from an Arch or Linux expert, most of what follows has been taken
from other sources. I link to where I found the information.

Next, keep in mind that Arch installations may vary slightly depending on the
machine you are trying to install it on. I strongly suggest trying to search the
Arch wiki for your target machine (e.g., [Dell XPS 13 7390 Arch Wiki](https://wiki.archlinux.org/index.php/Dell_XPS_13_(7390)).

Also, I acknowledge that I could have copied my existing Arch installation to the
target machine rather than manually setting everything up. However, I was interested
in documenting the steps of a fresh install as well as build up my scripts to make
it easier to do again in the future.

## Installing Arch on a USB from Another Arch Machine

### USB Storage Arch

Resource(s):
  + https://wiki.archlinux.org/index.php/USB_storage_devices

1. Find the device with `lsblk -f`
2. `mkdir /mnt/usb`
3. `mount -U <UUID> /mnt/usb`
4. When done, `umount /mnt/usb`

### Downloading the Arch `.iso`

Download the `*.iso` file from a mirror listed on the [Arch Downloads page (HTTP Direct Downloads)](https://www.archlinux.org/download/).

### Creating Bootable Arch image

Resource(s):
  + http://valleycat.org/linux/arch-usb.html?i=1

```bash
$ dd bs=4M if=$HOME/Downloads/archlinux.*.iso of=/dev/sda status=progress && sync
```

### Plug the USB into the Target Machine

Resource(s):
  + https://github.com/nw2190/Arch_Install

1. Enter the machine's BIOS menu. For me, smash `<F12>` while booting.

**CRITICAL:** in the BIOS, do the following:
  1. Disable `UEFI Secure Boot`
  2. Change the boot order to have the USB first
  3. Change the SATA operating mode from `RAID` to `AHCI`
    Your SSD should show when you boot arch with `lsblk -f`

Warmup complete. Level 1 unlocked.

---

## On the target machine

### Connect to WiFi

1. Make sure that the wireless drivers in the ISO were included and are supported

2. Connect to the WiFi
```bash
$ lspci -k | grep -A3 'Network controller'
$ iw dev
$ ip link set wlan0 up
$ iw dev wlan0 scan | grep 'SSID:'
$ wpa_supplicant -i wlan0 -c <(wpa_passphrase 'your_network_ssid' 'password')
```

> Once a connection is established, fork the process to the background by pressing `[CTRL]+z` and running `bg`.

3. Lease an IP address with `dhcpcd wlan0`
4. Sync system time with `timedatectl set-ntp true`

### Partitioning the Drive

1. `lsblk` to get the drive's name.

**CRITICAL:** Use the `UEFI/GPT` partitioning layout.
Specific details [here](https://wiki.archlinux.org/index.php/installation_guide)
and example layouts [here](https://wiki.archlinux.org/index.php/Partitioning#Example_layouts).
I originally was following [this post](https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd),
but my target machine would not allow "Legacy" boot mode (i.e., BIOS/MBR) in the BIOS.

Resources(s):
  + https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/
  + https://wiki.archlinux.org/index.php/installation_guide
  + https://wiki.archlinux.org/index.php/Partitioning#Example_layouts

2. Partition the drive with `fdisk`. You could also use `parted` or `gdisk`.
```bash
$ fdisk /dev/nvme0n1
$ (fdisk) g
$ (fdisk) n (skip, skip, +512M)
$ (fdisk) t (1, 1)
$ (fdisk) n (skip, skip, skip)
```

### Formatting the Partitions

Resource(s):
  +  https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
# Should show "esp" in Flags:
$ parted /dev/nvme0n1 print

# Initialize it as FAT32
$ mkfs.fat -F32 -nESP /dev/nvme0n1p1

# Initialize the root filesystem
$ mkfs.ext4 /dev/nvme0n1p2
```

### Encrypt the Drive

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ cryptsetup -c aes-xts-plain64 -y --use-random luksFormat /dev/nvme0n1p2
$ cryptsetup luksOpen /dev/nvme0n1p2 luks
```

### Logical Volume Manager (LVM) Partitions

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd
  + https://wiki.archlinux.org/index.php/LVM

```bash
$ pvcreate /dev/mapper/luks
$ vgcreate vg0 /dev/mapper/luks
$ lvcreate -L 8G vg0 -n swap
$ lvcreate -L 25G vg0 -n root
$ lvcreate -l 100%FREE vg0 -n home
```

### Format Partitions

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd
  + https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
$ mkfs.ext4 /dev/mapper/vg0-root
$ mkfs.ext4 /dev/mapper/vg0-home
$ mkswap /dev/mapper/vg0-swap
```

### Mount the Filesystem

Resource(s)
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ mount /dev/mapper/vg0-root /mnt
$ mkdir /mnt/{boot,home}
$ mount /dev/nvme0n1p1 /mnt/boot
$ mount /dev/mapper/vg0-home /mnt/home
$ swapon /dev/mapper/vg0-swap
```

### Install Packages that Go with You to the Root System

Resource(s)
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

**CRITICAL:** Install any packages that will help you with setup (e.g., packages
for connecting to WiFi). You could minimally install `base` and `base-devel`.

```bash
$ pacstrap -i /mnt \
  base \
  base-devel \
  linux \
  lvm2 \
  linux-firmware \
  nano \
  iw \
  dialog \
  dhcpcd \
  wpa_supplicant \
  git \
  vim \
  openssh \
  intel-ucode
```

### Generate `fstab`

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ genfstab -U /mnt >> /mnt/etc/fstab
```

### Enter the Root System

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ arch-chroot /mnt /bin/bash
```

1. Set timezone
```bash
# ln -s /usr/share/zoneinfo/America/New_York /etc/localtime
```

2. Set locale

```bash
$ vim /etc/locale.gen # (uncomment en_US.UTF-8 UTF-8)
$ locale-gen
$ echo LANG=en_US.UTF-8 > /etc/locale.conf
$ export LANG=en_US.UTF-8
```

3. Set hardware clock

```bash
$ hwclock --systohc --utc
```

4. Set hostname

Resource(s):
  + https://wiki.archlinux.org/index.php/installation_guide

```bash
$ echo dell-arch > /etc/hostname
```

`/etc/hosts`
```txt
127.0.0.1	localhost
::1        localhost
127.0.1.1	dell-arch.localdomain	dell-arch
```

5. Create a user

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd
  + https://wiki.archlinux.org/index.php/users_and_groups

```bash
$ useradd -m -g users -G wheel -s /bin/bash mccurdyc # the shell must be listed in $(cat /etc/shells)
$ passwd mccurdyc
$ visudo # uncomment %wheel ALL=(ALL) ALL
```

6. Configure `mkinitcpio` with modules needed for the `initrd` image

```bash
$ vim /etc/mkinitcpio.conf # Add 'encrypt' and 'lvm2' to HOOKS before 'filesystems'
$ mkinitcpio -p linux
```

7. Setup the `systemd-boot` boot manager

**CRITICAL:** `grub` didn't work

Resource(s):
  + https://www.cio.com/article/3098030/how-to-install-arch-linux-on-dell-xps-13-2016-in-7-steps.html
  + https://www.saminiir.com/installing-arch-linux-on-dell-xps-15/

```bash
# Make sure your ESP partition (described earlier) is mounted at /boot
$ mount -l | grep boot
$ bootctl --path=/boot install

# Get the UUID of your root partition
$ touch /boot/loader/entries/arch-encrypted-lvm.conf
$ blkid -s UUID -o value /dev/nvme0n1p2 >> /boot/loader/entries/arch-encrypted-lvm.conf
```

Add the following to `/boot/loader/entries/arch-encrypted-lvm.conf`

```
title Arch Linux Encrypted LVM
linux /vmlinuz-linux
initrd /intel-ucode.img
initrd /initramfs-linux.img
options cryptdevice=UUID=<UUID>:vg0 root=/dev/mapper/vg0-root quiet rw
```

### Reboot

1. Leave the root system with `exit`
2. `reboot`

If everything works, you've made it passed the hardest part! Level 2 unlocked.

---

## After Rebooting

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd
  + https://unix.stackexchange.com/questions/279545/failed-to-open-config-file-dev-fd-63-error-no-such-file-or-directory-for-wp

Make sure some things start on startup (and start them now).

```bash
$ systemctl enable dhcpcd.service
$ systemctl start dhcpcd.service
$ systemctl enable wpa_supplicant.service
$ systemctl start wpa_supplicant.service
```

### Reconnect to the WiFi

```bash
$ iw dev # the device name probably changed
$ sudo ip link set wlp2s0 up
$ sudo su -c 'wpa_supplicant -i wlp2s0 -c <(wpa_passphrase "your_network_ssid" "password")'
```

### Install Necessary and Helpful Packages

Resource(s):
  + https://gist.github.com/chrisleekr/a23e93edc3b0795d8d95f9c70d93eedd

```bash
$ pacman -S
  networkmanager \
  iw \
  zsh \
  wpa_supplicant \
  dialog \
  wireless_tools \
  base-devel \
  xclip \
  rofi \
  alacritty \
  netctl \
  fzf \
  tree \
  scrot \
  xdg-utils \
  bluez \
  bluez-utils \
  pulseaudio-bluetooth \
  pulseaudio-alsa
```

Make sure some more things start on startup (and start them now).

```bash
$ systemctl enable NetworkManager.service
$ systemctl start NetworkManager.service
$ systemctl enable bluetooth.service
$ systemctl start bluetooth.service
```

### Clone Helpful `git` Repositories

Set `zsh` as your default shell because the tools in `mccurdyc/dotfiles` expect this.

```bash
$ sudo chsh -s /bin/zsh mccurdyc
```

**CRITICAL:** This step creates the necessary symlinks and does the installations
and configuring described below.
```bash
$ git clone --recursive https://github.com/mccurdyc/dotfiles.git # ssh isn't configured yet
$ cd dotfiles && git submodule update --init
$ make run-minimal # does a bunch of necessary symlinking
$ export TOOLS_DIR=$HOME/tools
$ mkdir $TOOLS_DIR
```

Install [`yay`](https://github.com/Jguer/yay)
  + My favorite AUR package manager
  + Written in Go (I'd love to contribute)!
  + Actively maintained
  + Similar API to `pacman` (i.e., `-S` to install, `-R` to remove)

```bash
$ git clone https://aur.archlinux.org/yay.git $TOOLS_DIR/yay
$ cd $TOOLS_DIR/yay
$ makepkg -si
```

### Install Video Drivers

Resource(s):
  + https://wiki.archlinux.org/index.php/Intel_graphics

**CRITICAL:** `xf86-video-intel` caused video to be super super laggy in the next step!!!

```bash
$ pacman -S vulkan-intel vulkan-mesa-layer
```

### Install i3 Window Manager (and some other helpful packages)

```bash
$ pacman -S \
  xorg \
  xorg-xclock \
  xorg-twm \
  xorg-xinit \
  xterm \
  i3 \
  tmux \
  adobe-source-code-pro-fonts
```

```bash
$ yay -S \
  brave-bin \
  ttf-font-awesome # used by the i3status bar
```

**CRITICAL:** Important keystrokes. Remember these for when you are in the X window system.

+ The Windows key is set as the i3 modifier key (Mod)
    + Mod+Shift+Backspace - locks the screen (just start typing to login)
    + Mod+Shift+r - reloads the i3 config
    + Mod+`<ENTER>` - opens a terminal
    + Mod+Backslash (i.e., `\`) - opens a browser
    + Mod+`<TAB>` - brings up an application fuzzy searcher

To see all i3 keystrokes, check out [`~/.config/i3/config`](https://github.com/mccurdyc/dotfiles/blob/master/.config/i3/config).

```bash
$ startx # BAM! No longer limited to a shell.
```

If your video is super laggy or only updates on mouse movement, the `xf86-video-intel`
package is probably still installed. See the [Install Video Drivers section](#install-video-drivers).

```bash
$ pacman -R xf86-video-intel
```

If you have video and it's not laggy, you've made it passed the second most difficult part!
Final level unlocked. Time for the fun stuff (i.e., making it your own).

### Install Drivers

Resource(s):
  + https://www.archlinux.org/groups/x86_64/xorg-drivers/

```bash
$ pacman -S xorg-drivers
```

---

## After Device is Setup

Go ahead and reboot now with `sudo reboot -h now`.

### Adjusting Font Sizes

Resource(s):
  + https://wiki.archlinux.org/index.php/HiDPI

1. To adjust them in [GTK applications](https://wiki.archlinux.org/index.php/GTK)
(e.g., Chrome, Brave Browser, etc.), edit the font size in `~/.config/gtk-3.0/settings.ini`.

2. To adjust them globally and the actual browser content, update the font size in `~/.Xresources`,
but **more importantly, the `Xft.dpi` setting**.

Examples:

_Note: either export `QT_SCALE_FACTOR=...` or alias the commands to include the
application-specific scale factor._

```bash
$ QT_SCALE_FACTOR=2 zoom
```

Or, more likely, you will have to update the command that gets run by `/usr/local/share/application/<app-name>.desktop`.
To add user overrides, do the following:

```bash
$ export XDG_DATA_HOME="$HOME/.local/share"
$ cp /usr/local/share/applications/<application>.desktop $XDG_DATA_HOME
```

In order to prepend an environment variable --- like above --- you will have
to do the following, as noted in the "Modify environment variables" section in
[this Arch Wiki page](https://wiki.archlinux.org/index.php/Desktop_entries).

```bash
...
Exec=env QT_SCALE_FACTOR=2 /usr/bin/zoom %U
...
```

To read more about the XDG Base Directory, check out [this post on the Arch Wiki](https://wiki.archlinux.org/index.php/XDG_Base_Directory).

### Setup ssh for `git clone`

1. [Generate an SSH key](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

```bash
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa
$ xclip -sel clip < ~/.ssh/id_rsa.pub
```

2. [Add the SSH key to your GitHub account](https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account)

### Other Necessary Installs

Install `vim-plug` Plugin Manager for NeoVim

```bash
$ curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
$ nvim +PlugInstall +UpdateRemotePlugins +qall > /dev/null
```

`tmux` plugin manager

```bash
$ $(HOME)/.tmux/plugins/tpm/scripts/install_plugins.sh
$ tmux source $(HOME)/.tmux.conf
$ sudo npm i -g bash-language-server
```

To list packages on another Arch machine, run the following:

Official packages:
```
pacman -Qqne
```

AUR packages:
```
pacman -Qqme
```

### Optional Installs

```bash
$ pacman -S \
  docker \
  wget \
  imagemagick \
  htop \
  pavucontrol

$ yay -S \
  neovim \    # a "better" Vim editor
  hugo \      # static site generate written in Go
  python-grip # GitHub-flavored markdown previewer
```

---

## Other Notes

### Setting Default Applications

+ https://wiki.archlinux.org/index.php/XDG_MIME_Applications
+ https://www.linuxquestions.org/questions/slackware-14/wrong-application-for-opening-directories-with-xdg-open-4175619886/

```bash
$ xdg-mime query default inode/directory
```

### Screen Brightness

Resource(s):
+ https://prdpx7.github.io/linux/stuff-i-learned-while-fixing-brightness-on-ubuntu/
+ https://superuser.com/a/462828
+ https://unix.stackexchange.com/questions/471824/what-is-the-correct-substitute-for-rc-local-in-systemd-instead-of-re-creating-rc
+ https://www.linuxbabe.com/linux-server/how-to-enable-etcrc-local-with-systemd
+ digitalocean.com/community/tutorials/understanding-systemd-units-and-unit-files
+ https://bbs.archlinux.org/viewtopic.php?id=86815
+ https://wiki.archlinux.org/index.php/kernel_parameters

This one ultimately solved it for me
+ **https://wiki.archlinux.org/index.php/backlight**
>  If you find that changing the `acpi_video0` backlight does not actually change the brightness, you may need to use `acpi_backlight=none`.

```bash
$ ls /sys/class/backlight/
intel_backlight
```

Updated `/boot/loader/entries/arch-encrypted-lvm.conf` from [above](#enter-the-root-system) to include `acpi_backlight=none` in the `options`.

```
...
options ... acpi_backlight=none quiet rw
```

### Content Adaptive Brightness Control

Resource(s):
+ https://wiki.archlinux.org/index.php/Dell_XPS_13_(9360)#Content_Adaptive_Brightness_Control

Since I am on the Dell XPS 13 (7390), disabling Content Adaptive Brightness was
as easy as disabling it in the BIOS menu, under the Video settings.

### Bluetooth Audio

+ https://wiki.archlinux.org/index.php/Bluetooth
If you wanted a bluetooth GUI, you could install one of the suggested ones here.
+ https://wiki.archlinux.org/index.php/Bluetooth_headset
+ https://wiki.archlinux.org/index.php/PulseAudio

```bash
$ bluetoothctl
$ (bluetoothctl) power on
$ (bluetoothctl) agent on
$ (bluetoothctl) scan on
$ (bluetoothctl) devices
$ (bluetoothctl) pair <MAC>
$ (bluetoothctl) connect <MAC>
```

### Chrome Extensions

I wanted to also be able to install Chrome Extensions via the command line, but
it appears that this is not possible according to [this StackOverflow post](https://stackoverflow.com/questions/16800696/how-install-crx-chrome-extension-via-command-line).
The Chrome Extensions that I use are as follows:

+ [Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en)
+ [1 Password X](https://chrome.google.com/webstore/detail/1password-x-%E2%80%93-password-ma/aeblfdkhhhdcdjpifhhbdiojplfjncoa?hl=en)
+ [Notion Web Clipper](https://chrome.google.com/webstore/detail/notion-web-clipper/knheggckgoiihginacbkhaalnibhilkk/related?hl=en)

### Additional Resources

+ [i3status config](http://kumarcode.com/Colorful-i3/)
