---
title: "Cue Thoughts"
description: "I think it nailed the primary things I want in a configuration language; types, constraints, templating and preventing overrides. I think they've nailed the objectives, they just need to continue --- because they already have defined this as a clear focus --- improve the execution a bit."
author: ""
date: 2025-06-18T07:34:11-04:00
subtitle: ""
image: ""
post-tags: ["cue", "2025"]
posts: []
draft: false
---

I think it nailed the primary things I want in a configuration language; types, constraints, templating and preventing overrides. I think they've nailed the objectives, they just need to continue --- because they already have defined this as a clear focus --- improve the execution a bit.

They are still constantly improving the execution with new releases of the evaluator.

It's enjoyable to write. It has a bit of a learning curve related to disjunctions.

You physically cannot have value collisions so you will fight with this a bit if you use "fancy" things.

# What I like
- There's a playground - https://cuelang.org/play
- Types
- Constraints
- Feels like Go
- Integration with the Go ecosystem
- The Cue stdlib is just a Go package
	- https://cuelang.org/docs/tour/packages/standard-library/
	- https://pkg.go.dev/cuelang.org/go/pkg#pkg-overview
	- Has functions for strings, time, crytpo, encoding, net "strings" (IPs, subnets, etc.)
- Cue code generation (e.g., types) via `cue go import` (pointed at a Go package) or from protobuf types or jsonschema
- Modules (think Go packages) can be publishes as OCI artifacts
- Core maintainers are extremely responsive and get fixes cut fast!
- Can "inject" values from the CLI `--inject foo="foo"`

# The Learning Curve
- Disjunctions (i.e., value collisions / unset values)
	- https://cuelang.org/docs/tour/types/disjunctions/
- Think building a flat object
- String interpolation

    ```
    "Hello, \(Name)"
    ```

- Using templates; https://cuelang.org/docs/tour/types/templates/
- Notes I took when I was just learning - https://github.com/mccurdyc/playground/tree/main/cue#getting-started
- "unset" or "bottom" `_|_`
	- `if foo == _|_ {...}`
- There's `if`, but no `else`

# What to watch out for
Cue has a few things that are super powerful, but can lead to pain if abused. These can also be painful if the evaluator changes how it handles these things. You will likely spend a bit of time trying to produce a minimal reproducing example.

If you use "fancy" things sparingingly, I can't think of a downside of Cue.

In other words, introduce the fancy things like looping constructs, etc. sparingly.

- Looping constructs (i.e., `for` loops)
- Cue commands / "scripts" - https://cuetorials.com/patterns/scripts-and-tasks/
	- Can do filesystem thing
- The "function" pattern with loops

# Issues we've faced
At one point (early 2024) a `cue cmd` could take >10min (I think this is correct) to render a 10k line YAML file.

I think we starting using Cue around version 0.7.0. A ton has improved in the Cue internals since then; one of the biggest things is the new `evalv3` evaluation engine.

Most of this rendering time was due to us exposing a simple interface to configure Envoy. We wanted an interface like `{route: "/foo", backend: "foo"}`. Configuring a route and cluster in Envoy is ~200 lines of YAML and we have lots of routes, so we were doing loops and applying the "function" pattern to do transformations.

The big things that reduced rendering time. I don't have explanations for these things:
1. Moving from `cue cmd` to `cue eval -o yaml`
2. Moving many small packages to a more monolithic package (I wish I remembered more of the details because it wasn't just a package issue; it was likely looping and calling transforms across package lines)
