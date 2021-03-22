---
title: "Team Topologies"
subtitle: "Organizing Business and Technology Teams for Fast Flow"
description: "Team Topologies highlights human limitations regarding cognitive load and how this affects both system and organizational design. \"Team-first thinking\" is introduced as a foundational principle and is enabled via four fundamental team topologies -- stream-aligned, platform, enabling and complicated subsystem -- and three accompanying \"interaction modes\" —  X-as-a-Service, facilitating and collaborating. It is acknowledged that proper team topologies should be dynamic and evolve — not be blatantly copied — alongside the company and won't be as successful if the local and wider company culture is lacking in areas such as trust, emotional safety, vision, funding and abiding to industry best practices."
author: "Colton J. McCurdy"
date: 2021-03-22
image: ""
book-tags: ["book", "software engineering", "technology", "teams"]
books: ["Team Topologies"]
book-authors: ["Matthew Skelton", "Manuel Pais"]
amazon: "https://www.amazon.com/Team-Topologies-Organizing-Business-Technology/dp/1942788819"
---

<a href="https://teamtopologies.com/key-concepts" target="_blank">
  View on Team Topologies's website
</a>

<a href="https://web.devopstopologies.com/" target="_blank">
  Accompanying DevOps Topologies website
</a>

# Three-sentence Summary

Team Topologies highlights human limitations regarding cognitive load and how
this affects both system and organizational design. "Team-first thinking" is
introduced as a foundational principle and is enabled via four fundamental team
topologies -- stream-aligned, platform, enabling and complicated subsystem --
and three accompanying "interaction modes" -- X-as-a-Service, facilitating
and collaborating. It is acknowledged that proper team topologies should be
dynamic and evolve -- not be blatantly copied -- alongside the company and
won't be as successful if the local and wider company culture is lacking in
areas such as trust, emotional safety, vision, funding and abiding to industry
best practices.

# Personal Takeaways

> ... an organization is a socio-technical system or ecosystem that is shaped
by the interaction of individuals and the teams within it; in other words, ...
an organization is the interaction between people and technology [p. xxi]

The goal is to eventually reach a state where the overhead of cross-team
communication is reduced to interfacing with a simple, intuitive API that
accomplishes the task at hand without every team bearing the cognitive of every
system.

## Human cognitive limitations

Trust is fundamental to success.

### Anthropological research [p. 32, 33]

- ~5 person groups can hold close personal relations and working memory.
- ~15 person groups can experience deep trust.
- ~50 person groups can experience mutual trust.
- ~150 person groups can remember strengths and capabilities.

Psychologist, John Sweller defines three kinds of cognitive load which should
be addressed in the following order [p. 40]:

1. **extrinsic** - e.g., deploying or general toil tasks.
2. **intrinsic** - e.g., programming languages, technologies, etc.
3. **germane** - e.g., business logic / context

It's hard to quantify and assess a team's cognitive load [p 41]. Lines-of-code,
etc. are misaligned, so instead it's suggested using simple survey-type
questions such as, "do you feel like you're effective and able to respond in a
timely fashion to all work assigned to the team?"

## Stages of Team Evolution

*Developmental Sequence in Small Groups* by Bruce Tuckman identifies four
stages of team evolution [p. xxii]:

1. forming
2. storming
3. norming
4. performing

## Organizational and System Design

Organization designers need technical expertise because they are by proxy
defining system architecture [p. 23].

If you want to avoid centralization or single-points-of-failure (SPoF), then
design your teams as such. Specialized teams build centralized solutions [p.
21].

Restrict unnecessary communication. Not all communication and collaboration is
good [p. 24].

> Does the structure minimize the communication paths between teams? [p. 24]

If teams are communicating and they shouldn't be, the team's API (or platform)
is not doing its job [p. 25].

Many-to-many communication will produce tightly-coupled, interdependent,
monolithic systems [p 26].

> Every part of the software system needs to be owned by exactly one team [p.
37]

There should be no shared ownership of dependent parts. This doesn't mean that
teams shouldn't accept outside contributions, etc.

Work should never be "handed off" [p. 100]

### System Architects

Avoid "Architecture Teams" [p. 109]. Instead, have architects on individual
teams who meet regularly with architects from other teams and act as the "glue"
between teams. One goal of an architect should be to discover effective
cross-team APIs.

An architect should be much more than a software system designer. They should
primarily thinking about team interaction patters, etc. and have influence in
business domains [p. 148].

### Spotify Model [p. 63]

This is a frequently-referenced team model. Don't just adopt this model.
Evaluate your team communication patterns and evolve over time. Don't "jump" to
a "solution".

- **"squad"** - a fully-autonomous group of 5-9 people with cross-functional
skills (e.g., databases, deployment pipelines, application development, etc.)
- **"tribe"** - comprised of multiple squads in a similar domain. Squads are
aware of work being done by other squads in the tribe.
- **"chapter"** - groups of individuals with similar areas of expertise in the
tribe (e.g., databases, deployment pipelines, application development, etc.)
- **"guild"** - includes people from multiple tribes, chapters and squads. (I
haven't wrapped my head around this one yet, need to read more).

Chapters and guilds are the "glue" without sacrificing autonomy.

## Team-first Thinking

Team's consist of cross-functional skills and define an "API" for interfacing
with the *team* rather than individuals with particular experience. Often what
happens is that knowledge silos form because an individual becomes *the* expert
of a particular task and folks outside of the team who have historically gone
to this individual, continue to go to that individual to get that task
accomplished. Not only does this form knowledge silos, it hinders this
individual from doing other tasks — either due to cognitive load or context
switching costs.

Dan Pink's three elements of intrinsic motivation [p. 11]:

1. autonomy
2. mastery
3. purpose

"Team APIs" - define how to interface with the team. They should be defined
with the target audience being other teams [p. 48]. You should be able to
"point" folks to this API.

- What do we own
- How do we version and what do versions mean (promises)
- Usage documentation / how-to-guides
- Practices and principles (for internal and external contributions, etc.)
- Communication protocols (e.g., Slack channels, etc.)
- Roadmap, goals and priorities

Every team at AWS assumes that every other team becomes a potential
denial-of-service (DOS) attacker, which results in defined service levels,
quotas and throttling; to even internal users [p. 49].

Autonomy comes from external dependencies being non-blocking [p. 68]. Teams
should aim to create consumable, self-service components for things that could
possibly be a blocking dependency for another team either now or in the future
[p. 69].

> Sometimes we can remove or lessen dependencies on a specific teams by
breaking down their set of responsibilities and empowering other teams to take
some of them on [p. 74].

## Team Topologies

- **Stream-aligned**: end-to-end autonomy for a given domain. A majority of a
company's teams should be stream-aligned teams. Otherwise, it's probable that
too much work is focused on tasks that don't progress the company's value add
to the world.
- **Platform**: operates and maintains an API for accomplishing some tasks
without human interaction being a blocker.
- **Enabling**: teaches stream-aligned teams best practices and facilitates —
possibly via example proof-of-concepts — onboarding to existing platforms.
Enabling teams do not implement production solutions for teams, but are there
primarily to share and answer questions.
- **Complicated subsystem**: owns a part of the system that requires
specialized knowledge.

## "Interaction Modes"

- **X-as-a-Service**: an interface for accomplishing a task that is
"consumable" by teams with no human blockers.
- **Facilitating**: one team — often an "enabling" team — assisting another
team accomplish a task by informing them of existing platforms or best
practices.
- **Collaborating**: humans from multiple teams working closely together. Good
for low-latency discovery phases of a project, but very cognitively costly if
continued indefinitely. If overused, collaboration can mask or hide
deficiencies in underlying platforms or capabilities [p. 154].

> Collaborate on potentially ambiguous interfaces until the interfaces are
proven stable and functional [p. 149]... discover to establish [p. 161].

> Use [a]wkwardness in [t]eam [i]nteractions to [s]ense [m]issing
[c]ababilities and [m]isplaced [b]oundaries [p. 150].

## "Inverse [or Reverse] Conway Maneuver"

Conway's law tells us that system design and communication between systems
match organization design and communication. Therefore, rather than teams
designing systems to align with organization structure, focus should be put on
designing teams such that they match the desired system architecture [p. 10].

## Thinnest Viable Platform (TVP)

Focus on building the thinnest viable platform for today's problem and not
worrying about solving future problems [p. 101]. A majority of focus should be
put into how the interfaces and UX will evolve over time. Therefore, it is best
to provide a minimal, versioned API now and conservatively add to it as
necessary.
