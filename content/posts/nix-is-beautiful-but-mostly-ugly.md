---
title: "Nix Is Beautiful; But Mostly Ugly"
description: "The abstractions built on Nix (more specifically flakes) made Nix more complex, instead of simpler."
author: ""
date: 2025-12-15T07:24:58-05:00
subtitle: ""
image: ""
post-tags: ["nix", "2025"]
posts: []
draft: false
---

I've used Nix and NixOS since September 4th, 2022. And I still struggle with it.
I end up using or building a pattern that makes sense to me --- at one point in time --- then
just copy-paste that everywhere. I've taken [the Nixcademy course](https://nixcademy.com). I've
re-done Nix from first principles [here](https://github.com/mccurdyc/playground/tree/main/nix).
Either I'm just stupid or there are some incorrect --- or too many --- abstractions.

---

The problem and way Nix solves package / dependency management is beautiful i.e., the `/nix/store`.
I love that it forces you to understand your tool's system dependencies.

Everything else on top of that is pretty ugly.

I don't have a problem with Nix the language, honestly.

The abstraction sprawl of the Nix community --- specifically when it comes to Flakes --- makes using Nix awful.
It's a clear indication that the community can't come to any sort of design conclusion
of the correct way to do something. I think this is confirmed
by the indefinite "experiment" --- introduced in 2021 --- that is nix flakes.

## Flakes

Again, flakes solve a real problem with nix i.e., dependency pinning. I don't
know enough to strongly comment on the flake schema. Although my impression
is that it's the wrong abstraction. The flake schema is large. And it's unclear why.

Then, you've got a literal million abstractions on top of flakes that make it even
more confusing.

## Approach

_Generally_, I think using Nix to build is wrong. You've now forced every
consumer of your tool to install Nix. Don't do this. Let people handle dependencies
how they want. Make Nix an optional layer on top of your language tooling
and build tool.

If you want standardization across your company's repos for build tooling,
then I think this is when Nix for building is correct. Otherwise, it becomes
a maintenance burden.
