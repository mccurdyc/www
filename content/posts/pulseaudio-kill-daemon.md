---
title: "Pulseaudio Kill Daemon"
author: ""
type: ""
date: 2020-08-19T06:50:52-04:00
subtitle: ""
image: ""
post-tags: []
posts: []
---

```
$ ps -aux | rg 'pulseaudio'
mccurdyc    7570  2.6  0.0      0     0 ?        Zsl  Aug17  78:31 [pulseaudio] <defunct>
root     1878994  0.0  0.0  85364  8296 ?        D<   06:44   0:00 pulseaudio -D
```

https://askubuntu.com/questions/30891/is-there-any-way-to-kill-a-zombie-process-without-reboot
