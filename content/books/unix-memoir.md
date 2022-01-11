---
title: "UNIX"
subtitle: "A History and a Memoir"
author: "Colton J. McCurdy"
date: 2020-01-31
description: "Author, Brian Kernighan talks about the environment, his time at Bell Labs and the many cool projects surrounding Unix."
image: "/images/unix-memoir/cover.jpg"
book-tags: ["book", "2020", "unix-memoir"]
books: ["UNIX: A History and a Memoir"]
book-authors: ["Brian Kernighan"]
amazon: "https://www.amazon.com/UNIX-History-Memoir-Brian-Kernighan/dp/1695978552"
thriftbooks: "https://www.thriftbooks.com/w/unix-a-history-and-a-memoir_brian-w-kernighan/24296322/#isbn=1695978552&idiq=35079524"
---

> If nothing else, choices that might seem wrong-headed or perverse today can often
be seen as natural consequences of what was understood and could be accomplished
with the resources available at the time.

## Long-term View

AT&T / Bell Labs had a very long-term view and an "unfettered environment for exploration"
no matter how unconventional.

> I think that it would be easier to move Unix to another piece of hardware than to
rewrite an application to run under a different operating system - Dennis Ritchie

This was different from what was typical at the time. Software was written specifically
_for_ the hardware that it was run on. Primarily because a lot of software was
written in low-level language specific to the hardware. Conversely, Unix, was
re-written in C which could be compiled to low-level instructions specific for the hardware.

## Management

The lack of explicit management was standard practice at Bell Labs. Bells Labs
had a broad but clear mission, "universal service". There was a lot of trust that
people were interested in achieving this mission.

> ... no research proposals, no quarterly progress reports, and no need to seek
management approval before working on something.

> As Dick Hamming said, if you don't work on important problems, it's unlikely that
you'll do important work.

## The Culture

Brian talks about how he felt that he was a below-average intern after his final
year of college at Imperial Oil. He spent the entire summer _trying_ and failing
to get a COBOL program to analyze data. I personally have stories just like this
where I struggled early on in my programming career with what now seems obvious.
One task in particular that I remember receiving was to transform "large" JSON log
dumps. If I remember correctly, it took me roughly a month to write a program that
did this.

At Bell Labs, _everyone_, even the "famous" people, took time to listen to, speak
and work with, interns.

> Everyone gave generously of their time, it was simply part of the culture that you
provided detailed comments on what your colleagues wrote.

Writing was especially important at Bell Labs and the spread of both Unix and C.

Brian played an important role in the success of Unix and C by unofficially being, what the
industry now calls, a Developer Advocate. Writing that was published externally was
one of the primary recruiting mechanisms. Writing was part of the process that
was respected and given time at Bell Labs. There were close ties to academia and
you were expected to write papers, give talks and even teach courses at universities.

> External visibility was important for recruiting...Secretive companies had a harder
time attracting talent.

> We could only hire one or two people a year, and almost always young ones.

On whether Bell Labs was more interested in specialization or generalization, Steve
Johnson once asked, "should we be hiring athletes or first basemen?

Brian said that his preference was always for people who were good at what they did,
without worrying too much about what specifically it was.

## Constraints

> If nothing else, choices that might seem wrong-headed or perverse today can often
be seen as natural consequences of what was understood and could be accomplished
with the resources available at the time.

> If resources are tight, that's more likely to lead to good, well thought-out work
than if there are no constraints.

This was a major contributing factor to the design of Unix, but also a way to get
teams and departments to work together to collectively achieve some goal. The Unix
department tried to get funding for a new computer, specifically, to upgrade from the PDP-7
to the PDP-11. They were denied multiple times for funding.

Bell Labs had an active patent department and the Unix team knew that they were considering buying
new, expensive, patent-specific hardware. The Unix team saw this as an opportunity
to get what they wanted, a PDP-11. The Unix team convinced the patent department
to purchase a PDP-11 and the Unix team agreed to write the patent-printing software
for the general-purpose hardware. The patent printing department would use the hardware
during the day and the Unix team had free rein over the hardware in the evening
to build and test software. This became difficult because the patent department
relied on this hardware, so if the software broke, then the department couldn't work.
Keep in mind that this was before proper version control, so easily rolling back
to a working version of the software was difficult. Eventually, the patent department
bought a PDP-11 for the Unix department to build and test software.
