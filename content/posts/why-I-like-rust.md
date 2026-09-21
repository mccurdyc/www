---
title: "Why I Like Rust"
author: ""
type: ""
date: 2020-06-11T07:32:48-04:00
subtitle: ""
image: ""
post-tags: []
posts: []
---

How I approached learning Rust

Read [my cryptopals posts](), but personally, I think it would be extremely difficult
(I dislike saying impossible) to try to learn Rust just by looking at open-source projects and trying to learn
on the fly.

I read about half of the Rust 2018 book and skimmed through the rest before writing
or reading a single line of Rust.

The whole rust book is freely available online! I referred (still refer; because I'm still learning)
to it a ton!

1. Explictness
  1. Explicit trait implementations
    * This is something that I struggle with in Go's implicit interfaces.

  To me, it appears that Rust took what Go did well (e.g., docs, a centralized docs reference)
  and improved upon it. Or where Go lacked something (e.g., a

  The Rust compiler is amazing. When people say to treat it like pair programming you definitely can
  and not necessarily just to see compilation errors, but community best practices (e.g., mod.rs file).
  I trust that the compiler will identify improvements, so I don't have the cognitive
  load of worrying about or spend the time researching what popular projects do.

  I haven't been introduced to the borrowchecker yet, but I'm sure they will be as
  nice as the compiler. Yes, the personification was deliberate. Granted, I haven't
  worked on anything serious, just went through some of early cryptopal challenges
  (see my post here as to why I choose to do these to learn a new language).

  2. Explicit error types tripped me up

  I started with just using `Box<dyn Error>` everywhere.

  In my experience in Go, you more often return the plain `error` interface rather
  than a specific implementation of that interface. This does not seem to be the case
  in Rust.

  3. Explicit best practices for project structure encouraged by the toolchain and compiler
  e.g., consider moving to `mod.rs`.
  e.g., cargo new ...

  Coming to Go and lacking this is a huge barrier to overcome and often immediately sets
  developers back and upsets them. The barrier itself is to either learn through trial
  and error or check out a bunch of popular projects (which often don't follow the same
  structure because there is no defined structure).

2. Docs, Docs, more Docs.

Which collection should I use?

https://doc.rust-lang.org/std/collections/

There is a doc for that.

3. Openness of the community

Recorded videos on YouTube of the language core team meeting.

4. Overall (not just projects) the community _feels_ more active

This could be because I am actively learning and seeking a lot more out.

## Things that I don't like as much (not necessarily "dislike")

1. Many ways to do something

I actually appreciate Go's restrictions (e.g., one loop mechanism) unlike Rusts
expanded limits (e.g., functional with iterators, while, for, etc.)

2. Still a lot of moving parts

You encounter lots of experimental or recently-deprecated features.

3. GoDoc's Table of contents

Rust uses the sidebar, but the list of methods don't include the full method signature,
just the name, so you can't quickly see what accepts or returns what, you would have
to search.

## Am I going to use Rust in my day-to-day

Probably not. Because the Go community where I work is strong and I still have a
lot to learn from them and if a majority of developers "speak" Go, that is how
we can grow faster together. Rather than someone new to Rust trying to introduce
Rust. If there was something that obviously would benefit from using Rust, I would
consider introducing it. However, what's even more important than using what may be
the best tool for the job, is having the best support for the job.
