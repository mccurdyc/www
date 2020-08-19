---
title: "pavucontrol Stuck Establishing Connection to PulseAudio"
author: "Colton J. McCurdy"
date: 2020-08-19T06:50:52-04:00
subtitle: ""
image: ""
post-tags: ["pavucontrol", "linux", "arch", "pulseaudio", "debugging"]
posts: ["pavucontrol Stuck Establishing Connection to PulseAudio"]
---

## Overview

While fairly rarely --- like once every six months --- out of nowhere, I will lose audio.
The first thing I do is check out `pavucontrol`, which presents an otherwise blank
screen that says, "Stuck establishing connection to PulseAudio. Please wait...".

Let me just recommend that you don't just wait :) Or, if you do, don't wait more than
a few seconds before concluding that something else is wrong.

This post is mostly for myself to remember what to do in about six months when this
happens again. While I feel pretty confident that this will resolve the issue, I
had rebooted, which was my previous method for resolving this issue. It's super
annoying to have to rely on a reboot to resolve an issue, so my goal was to avoid
having to reboot.

## I just want the "answer"

This section is mostly for my future self who just wants to resolve the issue.

```bash
$ systemctl --user restart pulseaudio.service
```

## Debugging Process

Hey, look the pulseaudio process is "defunct"! [This askubuntu post](https://askubuntu.com/questions/201303/what-is-a-defunct-process-and-why-doesnt-it-get-killed)
describes what "debunct" means, "... the process has either completed its task or
has been corrupted or killed, but its child processes are still running or these parent process is monitoring its child process."

The usual `kill -9 PID` will not work for killing this process. Instead, you will
have to kill the parent process. This post suggests using `ps -ef` to identify the
parent process' PID (or PPID).

```bash
$ ps -aux | rg 'pulseaudio'

mccurdyc    7570  2.6  0.0      0     0 ?        Zsl  Aug17  78:31 [pulseaudio] <defunct>
root     1878994  0.0  0.0  85364  8296 ?        D<   06:44   0:00 pulseaudio -D
```

https://askubuntu.com/questions/30891/is-there-any-way-to-kill-a-zombie-process-without-reboot

When it's healthy it looks like the following:

```bash
$ ps -aux | rg 'pulseaudio'
mccurdyc    1206  1.8  0.1 1800072 16592 ?       S<sl 06:57   0:02 /usr/bin/pulseaudio --daemonize=no
mccurdyc    1285  0.0  0.0 235296  7020 ?        Sl   06:57   0:00 /usr/lib/pulse/gsettings-helper
```

I noticed that it had `--daemonize=no`, which would make it hard to debug when it fails via the `--check` or `-k` `pulseaudio` flags.

So I wanted to see where this flag was set. To do this, I had to identify the parent process (the PPID).

```bash
$ ps -ef | rg 'pulseaudio'
UID          PID    PPID  C STIME TTY          TIME CMD
...
mccurdyc    1206     899  6 06:57 ?        00:01:50 /usr/bin/pulseaudio --daemonize=no
mccurdyc    3921    2549  4 07:00 pts/8    00:01:19 nvim content/posts/pulseaudio-kill-daemon.md
```

Find more details about the parent process.

```bash
$ ps -aux | rg '899'
mccurdyc     899  0.0  0.0  19168 10160 ?        Ss   06:57   0:00 /usr/lib/systemd/systemd --user
```

Found it!

```bash
$ systemctl --user status pulseaudio.service
● pulseaudio.service - Sound Service
     Loaded: loaded (/usr/lib/systemd/user/pulseaudio.service; disabled; vendor preset: enabled)
     Active: active (running) since Wed 2020-08-19 06:57:38 EDT; 10min ago
TriggeredBy: ● pulseaudio.socket
   Main PID: 1206 (pulseaudio)
     CGroup: /user.slice/user-1000.slice/user@1000.service/pulseaudio.service
             ├─1206 /usr/bin/pulseaudio --daemonize=no
             └─1285 /usr/lib/pulse/gsettings-helper

Aug 19 06:57:35 fastly-arch systemd[899]: Starting Sound Service...
Aug 19 06:57:36 fastly-arch pulseaudio[1206]: W: [pulseaudio] alsa-ucm.c: UCM file does not specify 'PlaybackChannels' or 'CaptureChannels'fo>
Aug 19 06:57:36 fastly-arch pulseaudio[1206]: W: [pulseaudio] alsa-ucm.c: UCM file does not specify 'PlaybackChannels' or 'CaptureChannels'fo>
Aug 19 06:57:36 fastly-arch pulseaudio[1206]: W: [pulseaudio] alsa-ucm.c: UCM file does not specify 'PlaybackChannels' or 'CaptureChannels'fo>
Aug 19 06:57:38 fastly-arch systemd[899]: Started Sound Service.
```

```
$ bat /usr/lib/systemd/user/pulseaudio.service
───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: /usr/lib/systemd/user/pulseaudio.service
───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ [Unit]
   2   │ Description=Sound Service
   3   │
   4   │ # We require pulseaudio.socket to be active before starting the daemon, because
   5   │ # while it is possible to use the service without the socket, it is not clear
   6   │ # why it would be desirable.
   7   │ #
   8   │ # A user installing pulseaudio and doing `systemctl --user start pulseaudio`
   9   │ # will not get the socket started, which might be confusing and problematic if
  10   │ # the server is to be restarted later on, as the client autospawn feature
  11   │ # might kick in. Also, a start of the socket unit will fail, adding to the
  12   │ # confusion.
  13   │ #
  14   │ # After=pulseaudio.socket is not needed, as it is already implicit in the
  15   │ # socket-service relationship, see systemd.socket(5).
  16   │ Requires=pulseaudio.socket
  17   │ ConditionUser=!root
  18   │
  19   │ [Service]
  20   │ ExecStart=/usr/bin/pulseaudio --daemonize=no
  21   │ LockPersonality=yes
  22   │ MemoryDenyWriteExecute=yes
  23   │ NoNewPrivileges=yes
  24   │ Restart=on-failure
  25   │ RestrictNamespaces=yes
  26   │ SystemCallArchitectures=native
  27   │ SystemCallFilter=@system-service
  28   │ # Note that notify will only work if --daemonize=no
  29   │ Type=notify
  30   │ UMask=0077
  31   │
  32   │ [Install]
  33   │ Also=pulseaudio.socket
  34   │ WantedBy=default.target
───────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

Next time it fails, I am going to try restarting pulseaudio via `systemctl --user restart pulseaudio.service`.
