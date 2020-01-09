---
title: "Thinking in Systems"
subtitle: "A Primer"
author: "Colton J. McCurdy"
date: 2020-01-06
abstract: ""
book-tags: ["book", "2020", "systems-thinking"]
books: ["Thinking in Systems: A Primer"]
book-authors: ["Donella H. Meadows"]
---

{{% book author="Donella H. Meadows" amazon="https://www.amazon.com/Thinking-Systems-Donella-H-Meadows/dp/1603580557" thrift="https://www.thriftbooks.com/w/thinking-in-systems-a-primer_donella-h-meadows/258994/#isbn=1603580557&idiq=7108396" %}}
{{% /book %}}

> We can't control systems or figure them out. But we can dance with them!

# Mental Models of Systems

> Everything we think we know about the world is a model... None of this is or ever
will be the _real_ world.

Our models of the world and how things are interconnected are "pretty good", but
they are far from perfect and are incomplete. Additionally, these models are extremely
biased as we tend to ignore information that doesn't fit our current model. In order to
be successful, you must be willing to acknowledge that your views are just a model
and that you may be lacking information that someone else may have because of their
differing "viewpoint".

> Remember, always, that everything you know, and everything everyone knows, is only a model.

</br>
# System Composition

Systems are composed of elements, interconnections and functions or purposes. Often,
these elements aren't perfectly in sync, leading to a system that operates less
effectively or efficiently as possible. More generally, systems are composed
of "stocks" and "flows". Where stocks are the system's "memory" of the
changing inflows and outflows in a system.

A trivial system example is a single inflow, outflow and stock with no feedback. This can be
represented by a bathtub with a faucet, a drain and water flowing continuously,
rather than being turned down when the tub is getting full. If the
inflow is greater than the outflow, then the bathtub overflows. A real-world example
in the context of software engineering, is when tech debt is accumulated more
quickly than it is "paid", leading to unreliable and hard to maintain software systems.

Above, I explicitly stated "no feedback". Feedback loops are a significant component
of systems. These loops can be defined as managing flows in response to stock levels --- e.g.,
turning down the flow of water when the water is approaching the brim of the tub.
Feedback in a real-world system, again in the context of software engineering, could
be provided via Service-Level Objects (SLOs). Where if the "budget" is exceeded,
you shift focus from building new components to maintaining and hardening what currently exists.
The resiliency of a system is difficult to see _until_ you exceed its limits.

> Placing a system in a straitjacket of constancy can cause fragility to evolve. -C.S. Holling

> People often sacrifice resiliency ... for productivity, or for some other more
immediately recognizable system property.

Feedback loops can either be "reinforcing" or "balancing". Reinforcing feedback
loops can be either positive or negative and lead to compounded results, the "snowball
effect" or "success to the successful". Balancing or stabilizing feedback loops
work to pull elements to a steady state.

Often, feedback loops are part of many subsystems, _simultaneously_. Because these
feedback loops are fibers between subsystems, they help harmonize or sync subsystem
goals with macro system goals.

## Hierarchies of Systems: systems of systems

Systems are comprised of subsystems, which are also comprised of subsystems of
subsystems. There are efficiencies and inefficiencies that come from these hierarchies.
Subsystems help the macro system or encompassing subsystem by reducing the amount
of information and oscillations of change that need to be shared with the entire system.

> ... relationships _within_ each subsystem are denser and stronger than relationships
_between_ subsystems.

## Limiting Factors

Limiting factors are something determine how successful the overall system performs,
independent of how much is invested in improving other elements of the system.
An example of the "limiting factor" is that it doesn't matter how well built your
software is if you have a terrible product with no users. The product is your limiting
factor and where you should be focused.

> At any given time, the input that is most important to a system is the one that is
most limiting.

</br>
# Everything is part of a system, right? Wrong.

While reading this book, there were times when I would find myself thinking that
everything is part of _some_ system.

However, this statement is false. An entity is only part of a system
if there are affects caused by removing the entity. Elements, often the physical
entities of a system are the easiest part of a system to identify. The interconnections,
rules and goals of a system are much more difficult to _accurately_ identify.

> Purposes are deduced from behavior, not from rhetoric or _stated_ goals.

</br>
# (In-)Efficiencies of systems

## Competing Goals

Often, subunits or even subsystems may have a goal of their own that is being
optimized for, but this goal doesn't perfectly align or possibly unknowingly
works against the goal(s) of the macro system.

An example that came to mind when I read this was when an Engineering organization in a company is optimizing
for idealistic solutions and forgetting about the company goals _at that point in
time_. For example, idealistic solutions are less important when the company is
trying to establish product-market fit. Conversely, higher-quality solution may
be preferred to "hacky" solutions after establishing product-market fit.

## Centralized Control

Central control can be as damaging as subsystem optimizations. Conversely, "there must
be enough central control to achieve coordination toward the larger-system goal".

> ... there must be enough central control to achieve coordination toward the larger-system
goal, and enough autonomy to keep all subsystems flourishing, functioning and self-organizing.

## Ubiquitous Delays, "Buffers"

If the delays of information sharing are too short, they amplify short-term variation and create unnecessary
instability. This is one reason why hierarchies and the "guard" of information sharing
are necessary. In software engineering, engineering managers are necessary to
guard the individual contributors from receiving immediate, flucuating, information.

Later in the book, adding "buffers" is mentioned as a means to stabilize a system.
But, too big of buffers make systems slow and inflexible. Think of having to go
through many levels of management in order to be approved to make a change.

Optimizin  buffers, delays and the flow of information is usually an effective means to
improve a system. An example that comes to mind is when identifying software system
issues. If you don't have access to how your software is behaving, you won't know
what needs to be improved or how it is performing and you will probably end up
focusing on the wrong component. In software engineering this falls under "premature
optimization", by optimizing before profiling, etc.

> You can make a system work better with surprising ease if you can give it more timely,
more accurate, more complete information.

However, just because you _can_ measure something, doesn't mean that it _is_ important. Conversely,
because you _can't_ measure something, doesn't mean that it _isn't_ important.

Language is the primary means for sharing information and humans use it inefficiently and
ineffectively, often "polluting" information. As humans, we are inherently bad
at communicating and it requires a lot of practice and expertise in
something before we are able to effectively share ideas. The topic of
effective information sharing is discussed in Ben Orlin's [Math with Bad Drawings:
Illuminating the Ideas That Shape Our Reality](https://www.amazon.com/Math-Bad-Drawings-Illuminating-Reality/dp/0316509035),
where, Ben states that the difference between a good and
great mathematician is that a great mathematician is able to describe complex concepts,
simply.

> Honoring information means above all avoiding language pollution --- making the
cleanest possible use we can of language. Second, it means expanding our language
so we can talk about complexity.

Language is an example of a limiting factor. Think about when you are learning a new
language, whether it be the language of a another country or the language of a new
profession. You prefer to talk about the things that you know how to talk about
easily.

> ...we don't talk about what we can see; wee see only what we can talk about...

</br>
# "Linear minds in a non-linear world"

As humans, we tend to over-simply things. In the context of systems, we often
over-simplify the interconnections between elements. Systems don't have clear boundaries
and the interconnections are not linear or as direct as we may think. These artificial
boundaries are created in our minds and we become attached to them.

> You can't navigate well in an interconnected, feedback-driven world unless you take
your eyes off short-term events and look for long-term behavior and structure; unless
you are aware of false boundaries and bounded rationality; unless you take into account
limiting factors, non-linearities and delays.

## An Exaggerated Present

We often under- and over-estimate risk because of too much weight being put on
recent events and too little on historical behavior.

</br>
# Correcting Systems

Before changing or disturbing a system by attempting to correct it, observe its
behavior for a while. When observing behavior, prefer factual, historical reference
points to biased memories.

A common, and often early, approach to "correct" systems is to change the elements
of the system. This is one of the "cheaper" change to make and therefore, it usually
has a relatively low impact if the interconnections, rules and goals still exist
and are "broken". If changing an element in the system also causes a change
in relationships or functions, then the impact can be more significant. But these
major elemental changes tend to be more expensive than changing less impactful elements.

> Instead of asking who's to blame, you'll be asking "what's the system"?

In software engineering, one form of a factual reference
point could be Root Cause Analysis (RCA) documents. These RCA documents are great
reference points for newcomers to help them establish a mental model of the
system --- e.g., weak points, etc..

## An Event- versus Behavior-level Understanding

Events from a system are one of the most visible forms of output, but not the most
important. In order to understand the behavior of a system, observe how events
accumulate. This is the difference between an event- and behavior-level understanding
of a system. Event-level observations don't give you the ability to predict future
system behavior.

## Leverage Points

Leverage points are places in the system where "tweaks" can be made
to _try_ to improve or correct the system.
However, the leverage points that result in the desired behavior are not intuitive
and difficult to share.

One example is changing flows i.e., changing the "parameters".
Changing flows is often one of the first leverage points that is considered. While it is
relatively inexpensive, it frequently has little effect. Yet, this is where
most focus and time is spent when people try to
correct systems.

The most impactful leverage points are clearly defined, accurate goals
that are aligned with the rules and paradigm or mental model shifts.
