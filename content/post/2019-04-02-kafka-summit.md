---
title: Kafka Summit New York City 2019
author: "Colton J. McCurdy"
date: 2019-04-02
tags: ["kafka", "kafka summit", "nyc"]
posts: ["Kafka Summit New York City 2019"]
---

# Overview

The following will serve as my personal takeaways from my attendance of Kafka Summit
New York City 2019. This list is limited to the talks that I attended and my takeaways
from those talks.

For the full list of talks, provided talk summaries and the various tracks, visit
the [Schedule Page](https://kafka-summit.org/kafka-summit-new-york-2019/schedule/).
For more details about the event itself, visit the [Kafka Summity New York City 2019 Homepage](https://kafka-summit.org/events/kafka-summit-new-york-2019/).

---

## (Keynote) The Rise of Real-Time

Speaker(s):

  + Jay Kreps ([@jaykreps](https://twitter.com/jaykreps)): CEO, Co-Founder, Confluent
  + James Watters ([@wattersjames](https://twitter.com/wattersjames)): SVP, Strategy, Pivotal

### Key points:
+ transformations in many industries to be event-driven and immediately reactive
+ fundamental paradigm shift from how industries such as automobiles previously used data
+ event-driven is still in its infancy. Far from being as developed as persisting and querying data

---

## Building Scalable and Extendable Data Pipeline for Call of Duty Games: Lessons Learned

Speaker(s):

  + Yaroslav Tkachenko ([@sap1ens](https://twitter.com/sap1ens)): Software Architect, Activision


### Key points:

+ non-blocking writes --- enabled by default --- is working fine for them
+ batching by user and match
+ throttling and sampling
  + both can be configured dynamically through what sounded like environment variables
  + want to be able to throttle specific bad actor even when the cluster limits have not been met
  + their throttling system is an in-house tool
+ Kafka has configurable acknowledgment parameters for the producer
  + [Official Producer Configuration Documentation for Kafka 2.2](https://kafka.apache.org/documentation/#producerconfigs)
  + `acks=0`: the producer will not wait for any acknowledgment from the server at all. The record will be immediately added to the socket buffer and considered sent. No guarantee can be made that the server has received the record
  + `acks=1`: the leader will write the record to its local log but will respond without awaiting full acknowledgement from all followers
  + `acks=-1` or `acks:all`: the leader will wait for the full set of in-sync replicas to acknowledge the record. This guarantees that the record will not be lost as long as at least one in-sync replica remains alive
    + Yaroslav said that they didn't notice a major performance difference between `acks=all/-1` and `acks=1`
+ they use a proxy that they send messages to instead of directly to Kafka
  + abstracts away that messages are going to Kafka
  + helps with Kafka version upgrades (Yaroslav specifically mentioned upgrades to the producer)
+ Yaroslav said he was aware of a very well-known, big, company that didn't have auth in-front of their producers
  + but had extremely strict downstream message schemas
  + bad data gets thrown out
  + makes it easier to scale up (I don't really understand how this would help though)
+ be aware of consumer bottlenecks when large messages occur
  + takes time to de-serialize these messages, etc.
+ it's fine to use chained Kafka clusters
+ **establish a strict topic naming convention**:
    + previously, they had a bad naming convention (picture)
      + `$env.$source.$game_title_uuid.$category-$version`
    + every time a new game came out, they would have to create around 12 topics
      + previously, they had dynamic topic creation when trying to write and topic didn't exist
      + this made it hard to diagnose issues
    + create a committee that owns the decisions around naming, message schema etc.
      + _I heard this a few times in other talks also_
+ name topics like DB namespaces and tables (e.g., `marketplace.purchases`, `telemetry.matches`, `user.login`)
+ clean, simple topic names
+ message envelope
    + metadata includes message type (json, avro, etc) (picture)
      + helps with pulling schema from schema registry
      + helps for a clean de-serialization function

## Design Patterns and Pitfalls When Marrying an Event Driven Architecture with a RESTful Microservices Architecture at Tinder

### Speaker(s):

  + Kyle Bendickson ([@kbendickson](https://twitter.com/kbendickson)): Software Engineer, Data, Tinder

### Key points:

+ 90% cost savings when they switched from AWS Kinesis
+ not worried about WHO is interested in an event, just that someone might --- or eventually will --- be interested in a particular event
+ when doing synchronous REST calls, requests are limited to the highest latency downstream microservice request
+ batch processing with windowing (e.g., every 100 events do some calculation)
+ data governance committee for defining events

---

## The Migration to Event-Driven Microservices

### Speaker(s):

  + Adam Bellemare: Staff Data Engineer, Flipp

### Key Points:

+ decouple teams (loose coupling between teams)
  + defining metrics for clearly understanding cross-team dependencies
+ major advocates of strong message schemas
+ there is always a price to pay
  + price to the business (e.g., downtime, slow response times, etc.)
  + or, technical complexity and implementation costs
+ provide templates for the happy paths
  + if you don't every service and implementation will be unique
  + or engineers will just find some other service to copy and it may not necessarily be the one that they should have copied
+ moving away from the monolith
  + monolith is not allowed to consume from kafka, only produce
+ **DB table commits produces to an intermediate Kafka topic**
  + avoiding dual writes
  + other design patterns are mentioned in ([@TODO] link to another talk)
+ discusses the tradeoffs around denormalization of data versus joining
  + upstream denormalization (consumer does fewer joins)
  + this puts a lot --- or all --- of work on the team who owns the monolith
  + proposes using a proxy service for doing joins/"eventification" (like creating a DB view)
+ **governance committee**
    + defining core versus primitive events
+ centralizing calculations in proxy to the producer (budget example)
+ one event type per topic
  + how do they handle CRUD events?
  + he said they don't use CRUD events
+ how do they managing breaking schemas?
  + new topic and stop producing to the old topic
  + starting at same offset ("shift" to new topic)

---

## How Nubank Maintains Consistency for a Financial Event-Driven Architecture

### Speaker(s):

  + Iago Borges: Software Engineer, Nubank

### Key points:

+ mentions [datomic](https://www.datomic.com/)
  + [ACID](https://docs.datomic.com/cloud/transactions/acid.html)
+ defines consistency
  + says as a team you need to define consistency SLAs
  + "eventually consistent"

---

## Keeping Your Data Close and Your Caches Hotter

### Speaker(s):

  + Ricardo Ferreira ([@riferrei](https://twitter.com/riferrei)): Developer Advocate, Confluent

### My tweets:

https://twitter.com/McCurdyColton/status/1113159815113658369

### Key points:

+ "Data is only useful if it is _Fresh_ and _Contextual_"
+ KSQL demo with Alexa
  + plays song on Spotify, audience guesses on Twitter, KSQL query shows guesses and highlights winner, all live
+ description of a stream
+ caching design patterns (using Ricardo's name for them)
+ refresh ahead
   + Kafka Connect populates cache when producer writes to DB
   + Personal Thought: wouldn't this introduce race conditions?
      + data wouldn't be available for read do you just keep retrying?
      + it was mentioned in another talk that there would only be race conditions if the producer was also the consumer otherwise, it is just as if the data doesn't exist
+ refresh ahead/adapt
   + KSQL transformations to the data before writing to cache and delivery
+ write behind
   + write to cache and Kafka Connect writes to DB asynchronously
   + write once, consume many (polyglot consumers)
+ write behind/adapt
   + KSQL transformation on the data before DB write to conform to DB schema

---

## From a Million to a Trillion Events Per Day: Stream Processing in Ludicrous Mode

### Speaker(s):

  + Shrijeet Paliwal ([@shrjeet](https://twitter.com/shrijeet))

### Key points

+ most producers are running on embedded devices at Tesla
+ frequent processing latencies on the embedded devices (e.g., no network)
+ large payload requires persisting the message outside of Kafka and adding reference to Kafka event log
+ internal tool: offset to time conversions (using timestamp in metadata)
  + useful for graphing events over time
+ embarrassingly small number of instances (1M with one broker) and they do 1B messages (wouldn't give the exact number)
+ **primarily running out of the box configuration**
+ internal tool: manually editing offsets during/after incidents

---

## Kafka as an Event Store – Is It Good Enough?

### Speaker(s):

  + Guido Schmutz ([@gschmutz](https://twitter.com/gschmutz)): Solution Architect, Trivadis

### Key points:

+ **normalized data leads to many joins**
+ in a DB, you store the current state, but not how it has changed over time
+ if you want to be scalable, don't rely on the DB for populating read replica(s) (e.g., write triggers, etc.)
+ CQRS
  + Command Query Responsibility Segregation
  + handle writes and reads differently/separately
+ event sourcing
  + store state-changing events, not states
+ event store
  + option 1: events per account/customer
    + always replay from offset 0)
    + not great due to the number of topics necessary (i.e., one per user)
  + option 2: events per event type (e.g., Account, Customer)
  + option 3: one topic with all events
+ Kafka alone is not a great event store
  + need a way to persist or using Kafka streams for a streaming design
+ **avoid dual writes**

---

## Streaming Ingestion of Logging Events at Airbnb

### Speaker(s):

  + Hao Wang: Senior Software Engineer, Airbnb

### Key points:

  + overview of the architecture at Airbnb
  + showed some graphs
