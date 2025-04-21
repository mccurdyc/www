---
title: "Mathematical Theory of Communication"
subtitle: ""
description: ""
author: "Colton J. McCurdy"
date: 2025-04-17T12:12:41-04:00
image: "/images/book-covers/mathematical-theory-of-communication/cover.jpg"
book-tags: ["book", "2025", "tech"]
books: ["Mathematical Theory of Communication"]
book-authors: ["Claude E. Shannon", "Warren Weaver"]
amazon: ""
thriftbooks: "https://www.thriftbooks.com/w/the-mathematical-theory-of-communication_claude-shannon_warren-weaver/413716/?resultid=427ae8f5-6aed-4dad-8313-c32a4294102b#edition=4539584&idiq=26834489"
draft: false
---

I think that we have just scraped the surface of how to communicate effectively.

For example, few can get you into their mind like David Foster Wallace. If you think about it more
abstractly, there is a lot of upfront "training" or "priming" then the rest can move faster. An expensive start for an effective future.

Thinking about a lot about "local-first" software recently

pviii - distinct partitioning into sources, source encoders, channel encoders, channels and associated channel and source decoders.

pviv - communication systems with frequency of errors as small as desired for a given channel for any data rate less than the channel capacity. ... clearly establishes a limit on the communication rate that can be achieved over a channel.

p3 - entropy is related to "missing information"

<mark>
p4 - Three levels of Communication Problems

Level A. - How accurately can the symbols of communication be transmitted? (The technical problem)

Level B. - How precisely do the transmitted symbols convey the desired meaning? (The semantic problem)

Level C. - How effectively does the received meaning affect conduct in the desired way? (The effectiveness problem)
</mark>

p4 - If Mr. X is suspected not to understand what Mr. Y says, then it is theoretically no possible, by having Mr. Y do nothing but talk further

p5 - It may seem at first glance undesirably narrow to imply that the purpose of all communication is to influence the conduct of the receiver. ... effectiveness involves aesthetic considerations ... The effectiveness problem is closely interrelated with the semantic problem

p7 - The _information source_ selects a desired _message_ out of a set of possible messages ... The _receiver_ is a sort of inverse transmitter

p8 - How does one measure _amount of information?_ ... _information_ must not be confused with meaning ... the semantic aspects of communication are irrelevant to the engineering aspects

<mark>
p8 - this word information in communication theory relates not so much to what you _do_ say, as to what you _could_ say.
</mark>

p9 - information is a measure of one's freedom of choice

p9 the amount of information is defined, in the simplest cases, to be measured by the logarithm of the number of available choices. ... base 2 ... when there are only two choices, is proportional to the logarithm of 2 to the base 2.

How do you confidently determine the number of input choices?

p10 - probability plays in the generation of the message.

p11 - communication systems ... [are] governed by probabilities; and in fact by probabilities which are not independent, but which, at any stage of the process, depend upon the preceding choices. ... This probabilistic influence stretches over more than two words ... A system which produces a sequence of symbols ... according to certain probabilities
is called a _stochastic process_, and the special case of a stochastic process in which the probabilities depend on previous events, is called a _Markoff process_ or Markoff chain.

p11 - an ergodic process ... is one which produces a sequence of symbols which would be a poll-taker's dream, because any reasonably large sample tends to be representative of the sequence as a whole.

p13 - Having calculated the entropy (or the information, or the freedom of choice) of a certain information source, one can compare this to the maximum value this entropy could have ... this is called _relative entropy_ ... If the relative entropy of a certain source is, say 0.8, this roughly means that this source is, in its choice of symbols to for, a message, about 80 percent as free as it could possibly be with these same symbols. One minus the relative entropy is called the _redundancy_. ... this fraction of the message is unnecessary ... in the sense that if it were missing the message would still be essentially complete ... the redundancy of English is just about 50 percent, so that about half of the letters or words we choose in writing or speaking are under our free choice, and about half (although we are not ordinarily aware of it) are really controlled by the statistical structure of the language.


