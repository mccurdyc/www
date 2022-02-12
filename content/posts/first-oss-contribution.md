---
title: My Personal Journey to the Open Source Community
description: ""
author: "Colton J. McCurdy"
date: 2018-11-06
post-tags: ["open-source", "neighbor", "hacktoberfest", "golang"]
posts: ["My Personal Journey to the Open Source Community"]
---


{{< figure src="https://storage.googleapis.com/images.mccurdyc.dev/images/hacktoberfest-tshirt.jpg" >}}

For five years now, GitHub has been a part of the month-long celebration of open
source software, known as Hacktoberfest. Hacktoberfest is an opportunity for new and
veteran contributors to open pull requests on various projects across GitHub. During
this "trick-or-treat for hackers", maintainers of projects are extremely welcoming and love
to see new contributors to open source visit their projects. This was not only my
first time contributing during Hacktoberfest, but my first time contributing to an
open source project other than my own. However, it was my own project, [neighbor](https://github.com/mccurdyc/neighbor)
that inspired me to contribute to the project of choice, namely [source{d}'s](https://sourced.tech/)
[go-git](https://github.com/src-d/go-git).

## My personal open-source project

<p align="center">
  <img src="https://storage.googleapis.com/images.mccurdyc.dev/images/neighbor.png" width="300" height="300">
</p>

My personal project, [neighbor](https://github.com/mccurdyc/neighbor), is a
"neighborhood watch" for projects in the GitHub community. Users
create and run arbitrary shell commands or scripts on each project in the list
of cloned projects returned from a [GitHub search query](https://developer.github.com/v3/search/#search-repositories).
neighbor is an extensible means to enforce code quality on GitHub.

Due to the implementation of neighbor --- primarily the language choice, Go --- and
neighbor's tight coupling to GitHub via the API, discovering tools such as [Google's go-github](https://github.com/google/go-github)
and [source{d}'s go-git](https://github.com/src-d/go-git) was inevitable. While
querying GitHub's API certainly would have been possible without go-github, it
did add nice abstractions such as token authentication via OAuth2. On the other
hand, cloning projects would have consisted of numerous `git clone` shell commands via the
[`os/exec` package](https://golang.org/pkg/os/exec/); a much nastier problem to deal with. Not only this, but each
clone most-likely would have been its own [`Command`](https://golang.org/pkg/os/exec/#Command)
with the project under inspection as an argument.

## A quick shout-out to source{d}

<p align="center">
  <img src="https://storage.googleapis.com/images.mccurdyc.dev/images/sourced.jpg" width="400" height="150">
</p>

If you are unfamiliar with source{d}, you should check out what they are doing
on [their website](https://sourced.tech) and [GitHub profile](https://github.com/src-d).
At a high-level, source{d} is doing machine learning *on* code. To support this
mission, source{d} as an organization has created numerous tools, all of which are open source
under [source{d} proper](https://github.com/src-d) and the [Bablefish](https://github.com/bblfsh) organizations.

Not only do these tools help them achieve their goal of machine learning on code,
but most are built in such as way that they can be useful to those outside of
the source{d} organization, working on their own projects or research, such as myself.
Just to list a few of the projects: [engine](https://github.com/src-d/engine),
[gitbase](https://github.com/src-d/gitbase), and [lookout](https://github.com/src-d/lookout).
Admittedly, I have not had the opportunity to use all of these tools or investigate too deeply.

Next, something that I greatly appreciate about source{d} is the example they
set as an open and transparent organization, by including their [organizational documentation as
a public repository on GitHub](https://github.com/src-d/guide), something that [I mentioned
on Twitter](https://twitter.com/McCurdyColton/status/1041665070651125760) that we
started doing at StockX, except only internally.

Finally, everyone that I interacted with from source{d} was patient as I tossed
around ideas and helpful in pointing me in the right direction when I needed the
guidance, both on the [source{d} Slack](https://sourced-community.slack.com) and
in GitHub reviews. I honestly felt like part of the team.

## What is go-git?

<p align="center">
  <img src="https://storage.googleapis.com/images.mccurdyc.dev/images/go-git.png" width="700" height="200">
</p>

[go-git](https://github.com/src-d/go-git) is a "highly extensible Git implementation
in pure Go". In other words, go-git aims to be a feature-complete [git](https://git-scm.com/) implementation,
written entirely in Go. This is a huge contribution to the Go community! Having a
well-written and maintained package such as go-git available in any language would
be amazing, let alone my favorite language, Go!

## Why did I choose to contribute to go-git?

As a matter of fact, it was more like the issues chose me. While working on my
project, neighbor, specifically around authenticating with GitHub, I encountered
a few challenges. After using go-github, which supported OAuth2 for authentication,
I had the expectation that I would do something similar in go-git, namely use token
authentication, but this was not the case. It wasn't until I opened an [issue on
go-git](https://github.com/src-d/go-git/issues/999) and had a conversation with
one of the core maintainers of the project, Santiago M. Mola ([GitHub: @smola](https://github.com/smola), [Twitter: @mola_io](https://twitter.com/mola_io?lang=en)),
that I realized and accepted that [GitHub advises using basic authentication](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/)
(i.e., username, "password") for token authentication via personal access tokens.

To help others ([Issue#618](https://github.com/src-d/go-git/issues/61), [Issue#730](https://github.com/src-d/go-git/issues/73))
in the future who encounter the same confusion that I faced, [I created a few examples](https://github.com/src-d/go-git/pull/990)
for basic authentication with a password and personal access token.

After that, I was pumped and ready for more. I wanted to solve an issue that had
been open for a while on one of source{d}'s projects. I felt most comfortable
in and knowledgable of go-git, so that is where I started the search. In the issue
tracker on go-git, I came across [Issue#969](https://github.com/src-d/go-git/issues/969)
which had been open for almost 30 days, had no activity and was on a topic that
I had just recently been formally introduced to. I knew this issue was for me!
Only a few weeks prior, I was formally introduced to "flaky" tests by a colleague of mine who sent
me a [paper by Jonathan Bell of Carnegie Mellon University, et al.](https://www.jonbell.net/icse18-deflaker.pdf).
Bell et al. formally discuss flaky tests and propose a tool, DeFlaker, for automatically
detecting flaky tests.

Flaky tests often lead to untrusted or misleading tests and are arguably worse
than no test. Was that most recent change honestly the reason that the test failed?
Or, was it because the flakiness of the test was triggered? While discussing
flaky tests in detail is not in the scope of this post, one final key point made in the Bell
et al. paper is important to my story. "The typical way to detect flaky tests is to rerun
failing tests repeatedly", which was exactly what I did to solve [Issue#969](https://github.com/src-d/go-git/issues/969).

I found the cause of the flaky test using the exact method discussed in the paper
by Bell et al., a [simple script](https://gist.github.com/mccurdyc/5b39f971a122544e02e1e21c639a1e67)
that ran `go test` continuously, for a max of 5000 iterations with the same flags
as the CI of the go-git project enabled, looking for a failing test case. As simple
as this script may be, it ultimately helped me identify the root of the flakiness,
which ended up being a race condition where a resource was being closed prior to
writing to the resource being completed.

If you are wondering why I didn't use the [Go race detector](https://blog.golang.org/race-detector),
you are asking a great question! Ultimately, the reason was because I didn't want
to pull the necessary code out into an isolated demo project. Looking back, I probably
should have done this. Or at least ran the tests with the `-race` flag enabled.

## Conclusion

This year's Hacktoberfest marked the first time that I contributed to an open
source project other than my own. However, it was my own project that provided me
with the challenges personally to then want to help others. The project that I
contributed to was just one of many great projects from the creating organization,
namely source{d}. The issues that I solved were either related to a problem that
I personally encountered or had recently read a research paper about and was excited
to learn more. Everyone that I worked with or spoke to from source{d} was welcoming
of new ideas and patient with me as a new contributor to open source.

While I do plan to take a month break from contributing to other open source projects,
to continue making progress on my own personal projects, write more and spend time
with family during the upcoming holiday, I will certainly be contributing again
in the near future and go-git will be the first project that I visit.

If you are new to open source or are looking to solve your first issue on a project
other than your own, I'd love to talk! You can find my contact information on
the [Contact page](/contact). If you are interested in
formal research that I have done, check out the [Papers page](/papers).
