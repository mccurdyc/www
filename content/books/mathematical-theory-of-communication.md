---
title: "Mathematical Theory of Communication"
subtitle: ""
description: "[T]his word information in communication theory relates not so much to what you _do_ say, as to what you _could_ say. ... If it is not possible or practible to design a system which can handle everything perfectly, then the system should be designed to handle well the jobs it is most likely to be asked to do, and should resign itself to be less efficient for the rare task."
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

# SOME RECENT CONTRIBUTIONS: WEAVER

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

<mark>
p14 - If it is not possible or practible to design a system which can handle everything perfectly, then the system should be designed to handle well the jobs it is most likely to be asked to do, and should resign itself to be less efficient for the rare task.
</mark>

p15 - no freedom of choice --- no information

<mark>
p16 - the capacity of a channel [_C_] is to be described not in terms of the number of _symbols_ it can transmit, but rather in terms of the _information_ it transmits.
</mark>

p17 - _H_ bits per symbol ... no matter how clever the coding, can never be made to exceed _C/H_.

p18 - The greater this freedom of choice, and hence the greater the information, the greater is the uncertainty that the message actually selected is some particular one ... _Noise_

p22 - When there is noise on a channel, however, there is some real advantage in not using a coding process that eliminates all of the redundancy. For the remaining redundancy helps combat the noise.

p27 - The concept of information developed in this theory at first seems disappointing and bizarre --- disappointing because it has nothing to do with meaning ... one is now, perhaps for the first time, ready for a real theory of meaning.

<mark>
p28 - one of the most significant but difficult aspects of meaning, namely the influence of context.
</mark>

# THE MATHEMATICAL THEORY OF COMMUNICATION

p31 - the effect of noise in the channel, and the savings possible due to the statistical structure of the original message

p34 - We may roughly classify communication systems into three main categories: discrete, continuous and mixed.

## Discrete

p39 - reducing the required capacity of the channel, by the use of proper encoding of the information

p41 - _n_-gram - set of transition probabilities

p49 - These probabilities are known but that is all we know concerning which event will occur. Can we find a measure of how much "choice" is involved in the selection of the vent or of how uncertain we are of the outcome?

In other words, given the input probabilities can we reliably predict outcomes?

p62 - The transducer which does the encoding should match the source to the channel in a statistical sense. ... In general, ideal or nearly ideal encoding requires a long delay in the transmitter and receiver. ... the main function of this delay is to allow reasonably good matching of probabilities to corresponding lengths of sequences.

<mark>
p62 - If a source can produce only one particular message its entropy is zero, and no channel is required. ... No channel is required to "transmit" this to another point. One could construct a second machine to compute the same sequence at the point.
</mark>

p67 - The conditional entropy `H_y(x)` will, for convience, be called the equivocation. It measures the average ambiguity of the received signal. ... _a posteriori_ probability

p81 is where I stopped following along at a deeper level.

## CONTINUOUS INFORMATION

p81 - dividing the continuum of messages and signals into a large but finite number of small regions and calculating the various parameters involved on a discrete basis.

p85 - _The Interpolation, Extrapolation, and Smoothing of Stationary Time Series_ (Wiley, 1949), contains the first clear-cut formulation of communication theory as a statistical problem

## THE RATE FOR A CONTINUOUS SOURCE

p108 - In the case of a discrete source of information we were able to determine a definite rate of generating information, namely the entropy of the underlying stochastic process. With a continuous source the situation is considerably more involved. ... exact transmission is impossible. ... Practically, we are not interested in exact transmission when we have a contiuous source, but only in transmission within a certain tolerance.

p111 - The structure of the ear and brain determine implicitly a number of evaluations, appropriate in the case of speech or music transmission.
