---
title: "Documentation Is a Bandaid"
description: "Documentation is a bandaid for bad or hidden interface boundaries. Documentation is NOT a source of truth."
author: ""
date: 2024-08-07T07:59:30-04:00
subtitle: ""
image: ""
post-tags: ["documentation", "software engineering"]
posts: []
draft: false
---

Documentation is a bandaid for bad or hidden interface boundaries.

The following came to mind when I inherited an old system and was asked to make
significant changes to the system. I wanted to build my mental model up from a
source of truth and I didn't trust the docs.

Admittedly, not all documentation is a bandaid. You need some docs. But when you
need extensive documentation it's because processes or architecture is no intuitive
or accessible.

- treat docs as breadcrumbs; NOT sources of truth (even if your docs are generated from code comments. Comments often get outdated).
- systems should be built and have tooling so that you dont need (many) docs
- documentation is a great first step for highlighting and sharing a problem.
    - "Look, we have to run 42 commands to do X"
    - New person joins looking for how they can contribute to the project; "hey look, I know how to solve this!"
