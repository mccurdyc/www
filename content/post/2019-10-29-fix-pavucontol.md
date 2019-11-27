---
title: Fixing `pavucontrol`
author: "Colton J. McCurdy"
date: 2019-10-29
post-tags: ["linux", "pavucontrol", "audio", "2019"]
posts: ["Fixing `pavucontrol`"]
---

## Problem

I run Arch Linux on my personal machine. I love the configurability and that it
forces you to understand Linux and how things work. With Arch, things don't "just work",
you have to make them work. However, there are a lot of opportunities to also incorrectly
configure things, which is exactly what I did with my audio. Audio would work ---
i.e., I could change volume, mute, etc. --- but, I could not change I/O devices
using `pavucontrol`. You don't need `pavucontrol` to control I/O, but it is a nice
UI for handling this.

I learned a lot in the process of fixing `pavucontrol` on my machine.

`alsa` is a kernel space tool, `pulseaudio` is a user space tool for interacting with
`alsa`. A lot of applications require `pulseaudio`, but you can get away with lighter alternatives.

## The Fix
1. Update Related Dependencies
```bash
pacman -Syu pulseaudio, pulseaudio-alsa, pulseaudio-bluetooth, alsa-lib, alsa-utils, alsa-firmware
```

2. Update (Re-sync) the PulseAudio Config

What I finally did was make sure that the PulseAudio config for the current use
was in sync with root. To do this, I did the following:

1. `sudo cp -r /etc/pulse ~/.config/`
2. `pushd ~/.config/pulse && sudo chown -R <username> .`
3. then in ~/.config/pulse/client.conf, made sure that `autospawn = yes`
4. `pulseaudio --start`
5. `pavucontrol` started working!

## References
+ Huge shoutout to [this post](https://learn.foundry.com/nuke/content/timeline_environment/managetimelines/audio_pulse.html)
+ [This was another helpful post](https://linuxhint.com/pulseaudio_arch_linux/) which first exposed me to the user vs root config files
and other alternatives to pulseaudio, if I decided to go that route.
