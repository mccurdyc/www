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

## System composition

Systems are composed of elements, interconnections and functions or purposes. Often,
these elements aren't perfectly in sync, leading to a system that operates less
effectively or efficiently as possible.

More generally, systems are composed of "stocks" and "flows". Where stocks are the
system's "memory" of the changing inflows and outflows in a system. A trivial
system example is a single inflow, outflow and stock with no feedback. Think of
a bathtub with a faucet, a drain and being filled with water continuously. If the
inflow is greater than the outflow, then the bathtub overflows. A real-world example
in the context of software engineering may be where tech debt is accumulated more
quickly than it is "paid", leading to unreliable and hard to maintain software systems.

Above, I explicitly stated "no feedback", feedback loops are a significant component
of systems. These loops can be defined as managing flows in response to stock levels.
Another real-world example in the context of software engineering would be Service-Level
Objects (SLOs). Where if the "budget" is exceeded, you shift focus from building
new to maintaining and hardening what currently exists. The resiliency of a system
is difficult to see _until_ you exceed its limits.

> Placing a system in a straitjacket of constancy can cause fragility to evolve. -C.S. Holling

> People often sacrifice resiliency ... for productivity, or for some other more
immediately recognizable system property.

### Models of Systems

> Everything we think we know about the world is a model... None of this is or ever
will be the _real_ world.

Our models of the world and how things are interconnected are "pretty good", but
they are far from perfect and are incomplete.

### Hierarchies of Systems: systems of systems

Systems are comprised of subsystems, which are also comprised of subsystems of
subsystems. There are efficiencies and inefficiencies that come from hierarchies.
Subsystems help the macro system or next layer in the system by reducing the amount
of information and oscillations of change that needs to be shared with the whole system.

> ... relationships _within_ each subsystem are denser and stronger than relationships
_between_ subsystems.

### Feedback loops

Feedback loops can either be "reinforcing" or "balancing". Reinforcing feedback
loops can be either positive or negative and lead to compounded results, the "snowball
effect". Balancing or stabilizing feedback loops work to pull elements to a steady state.

Often, feedback loops are part of many subsystems, _simultaneously_.

### Everything is part of a system, right? Wrong.

While reading this book, there were times when I would find myself thinking that
everything is part of _some_ system. However, this is false. An entity is only part of a system
if there are affects caused by removing the entity. Elements, often the physical
entities of a system are the easiest part of a system to identify. The interconnections,
rules and goals of a system are much more difficult to _accurately_ identify.

> Purposes are deduced from behavior, not from rhetoric or _stated_ goals.

### (In-)Efficiencies of systems

Often, subunits or even subsystems may have a goal of their own that is being
optimized for, but this goal doesn't perfectly align or possibly unknowingly
works against the goal(s) of the larger, macro system. An example that came to
mind when I read this was when an Engineering organization in a company is optimizing
for idealistic solutions and forgetting about the company goals at that point in
time. For example, idealistic solutions are less important when the company is
trying to establish product-market fit.

Central control can be as damaging as subsystem optimizations. Conversely, "there must
be enough central control to achieve coordination toward the larger-system goal".

> ... there must be enough central control to achieve coordination toward the larger-system
goal, and enough autonomy to keep all subsystems flourishing, functioning and self-organizing.

### "Linear minds in a non-linear world"

As humans, we tend to over-simply things. In the context of systems, we often
over-simplify the interconnections between elements.

> You can't navigate well in an interconnected, feedback-driven world unless you take
your eyes off short-term events and look for long-term behavior and structure; unless
you are aware of false boundaries and bounded rationality; unless you take into account
limiting factors, non-linearities and delays.

## Correcting Systems

An approach that is when attempting to "correct" a system is to change the elements
of the system. This is one of the "cheaper" moves to make and therefore, it usually
has a relatively low impact if the interconnections, rules and goals are still
"broken" and in place. If changing an element in the system also causes a change
in relationships or functions, than the impact is more significant.

> Instead of asking who's to blame, you'll be asking "what's the system"?

Events from a system are one of the most visible forms of output, but not the most
important. In order to understand the behavior of a system, observe how events
accumulate. This is the difference between an event- and behavior-level understanding
of a system. Event-level observations don't give you the ability to predict future
system behavior.
