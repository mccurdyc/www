---
title: Kafka Summit New York City 2019
author: "Colton J. McCurdy"
date: 2019-04-02
tags: ["kafka", "kafka summit", "nyc", "conference", "2019"]
posts: ["Kafka Summit New York City 2019"]
image: /images/kafka-summit-nyc-2019.jpg
---

# Overview

The following will serve as my personal takeaways from my attendance of Kafka Summit
New York City 2019. This list is limited to the talks that I attended and my takeaways
from those talks.

For the full list of talks, provided talk summaries and the various tracks, visit
the [Schedule Page](https://kafka-summit.org/kafka-summit-new-york-2019/schedule/).
For more details about the event itself, visit the [Kafka Summity New York City 2019 Homepage](https://kafka-summit.org/events/kafka-summit-new-york-2019/).

The official videos and slides can be found [here](confluent.io/resources/kafka-summit-new-york-2019/).



---

## (Keynote) The Rise of Real-Time

Speaker(s):

  + Jay Kreps ([@jaykreps](https://twitter.com/jaykreps)): CEO, Co-Founder, Confluent
  + James Watters ([@wattersjames](https://twitter.com/wattersjames)): SVP, Strategy, Pivotal

### Video and Slides:

+ https://www.confluent.io/kafka-summit-NY19/events-everywhere

### Key points:
+ transformations in many industries to be event-driven and immediately reactive
+ fundamental paradigm shift from how industries such as automobiles previously used data
+ event-driven is still in its infancy. Far from being as developed as persisting and querying data

---

## Building Scalable and Extendable Data Pipeline for Call of Duty Games: Lessons Learned

Speaker(s):

  + Yaroslav Tkachenko ([@sap1ens](https://twitter.com/sap1ens)): Software Architect, Activision

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/call-of-duty-games

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/cod-proxy.jpg" caption="Slide 1" >}}
  {{< figure thumb="-thumb" src="/images/cod-chained-cluster.jpg" caption="Slide 2" >}}
  {{< figure thumb="-thumb" src="/images/cod-topic-naming.jpg" caption="Slide 3" >}}
  {{< figure thumb="-thumb" src="/images/cod-message-envelope.jpg" caption="Slide 4" >}}
{{< /gallery >}}

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
+ [Slide 1]: they use a proxy that they send messages to instead of directly to Kafka
  + abstracts away that messages are going to Kafka
  + helps with Kafka version upgrades (Yaroslav specifically mentioned upgrades to the producer)
+ Yaroslav said he was aware of a very well-known, big, company that didn't have auth in-front of their producers
  + "Simple rule for high-performant producers? Just write to Kafka, nothing else. [not even auth]"
  + but had extremely strict downstream message schemas
  + bad data gets thrown out
  + makes it easier to scale up (I don't really understand how this would help though)
+ be aware of consumer bottlenecks when large messages occur
  + takes time to de-serialize these messages, etc.
+ [Slide 2]: it's fine to use chained Kafka clusters
+ **establish a strict topic naming convention**:
    + previously, they had a bad naming convention (picture)
      + `$env.$source.$game_title_uuid.$category-$version`
    + every time a new game came out, they would have to create around 12 topics
      + previously, they had dynamic topic creation when trying to write and topic didn't exist
      + this made it hard to diagnose issues
    + create a committee that owns the decisions around naming, message schema etc.
      + _I heard this a few times in other talks also_
+ [Slide 3]: name topics like DB namespaces and tables (e.g., `marketplace.purchases`, `telemetry.matches`, `user.login`)
+ clean, simple topic names
+ [Slide 4]: message envelope
    + metadata includes message type (json, avro, etc) (picture)
      + helps with pulling schema from schema registry
      + helps for a clean de-serialization function

## Design Patterns and Pitfalls When Marrying an Event Driven Architecture with a RESTful Microservices Architecture at Tinder

### Speaker(s):

  + Kyle Bendickson ([@kbendickson](https://twitter.com/kbendickson)): Software Engineer, Data, Tinder

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/event-driven-architecture-restful-microservices

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/tinder-event-driven-arch.jpg" caption="Slide 1" >}}
  {{< figure thumb="-thumb" src="/images/tinder-notification.jpg" caption="Slide 2" >}}
{{< /gallery >}}

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

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/the-migration-to-event-driven-microservices

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/flipp-contexts.jpg" caption="Slide 1" >}}
  {{< figure thumb="-thumb" src="/images/flipp-dual-write.jpg" caption="Slide 2" >}}
  {{< figure thumb="-thumb" src="/images/flipp-dual-write2.jpg" caption="Slide 3" >}}
  {{< figure thumb="-thumb" src="/images/flipp-denormalization.jpg" caption="Slide 4" >}}
  {{< figure thumb="-thumb" src="/images/flipp-upstream-denormalize.jpg" caption="Slide 5" >}}
  {{< figure thumb="-thumb" src="/images/flipp-proxy-denormalization.jpg" caption="Slide 6" >}}
  {{< figure thumb="-thumb" src="/images/flipp-core-event.jpg" caption="Slide 7" >}}
{{< /gallery >}}

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
  + [Slides 2-3]: avoiding dual writes
  + other design patterns are mentioned in _Keeping Your Data Close and Your Caches Hotter_
+ [Slides 4]: discusses the tradeoffs around denormalization of data versus joining
  + [Slide 5]: upstream denormalization (consumer does fewer joins)
  + this puts a lot --- or all --- of work on the team who owns the monolith
  + [Slide 6]: proposes using a proxy service for doing joins/"eventification" (like creating a DB view)
+ **governance committee**
    + defining core versus primitive events
+ [Slide 7]: centralizing calculations in proxy to the producer (budget example)
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

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/maintaining-consistency-for-financial-event-driven-architecture

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

### My tweets

{{< tweet 1113159815113658369 >}}

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/keeping-your-data-close-and-your-caches-hotter

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/confluent-alexa.jpg" caption="Slide 1" >}}
  {{< figure thumb="-thumb" src="/images/confluent-refresh-ahead.jpg" caption="Slide 2" >}}
  {{< figure thumb="-thumb" src="/images/confluent-refresh-ahead-adapt.jpg" caption="Slide 3" >}}
  {{< figure thumb="-thumb" src="/images/confluent-write-behind.jpg" caption="Slide 4" >}}
  {{< figure thumb="-thumb" src="/images/confluent-write-behind-adapt.jpg" caption="Slide 5" >}}
{{< /gallery >}}


### Key points:

+ "Data is only useful if it is _Fresh_ and _Contextual_"
+ [Slide 1]: KSQL demo with Alexa
  + plays song on Spotify, audience guesses on Twitter, KSQL query shows guesses and highlights winner, all live
+ description of a stream
+ caching design patterns (using Ricardo's name for them)
+ [Slide 2]: refresh ahead
   + Kafka Connect populates cache when producer writes to DB
   + Personal Thought: wouldn't this introduce race conditions?
      + data wouldn't be available for read do you just keep retrying?
      + it was mentioned in another talk that there would only be race conditions if the producer was also the consumer otherwise, it is just as if the data doesn't exist
+ [Slide 3]: refresh ahead adapt
   + KSQL transformations to the data before writing to cache and delivery
+ [Slide 4]: write behind
   + write to cache and Kafka Connect writes to DB asynchronously
   + write once, consume many (polyglot consumers)
+ [Slide 5]: write behind adapt
   + KSQL transformation on the data before DB write to conform to DB schema

---

## From a Million to a Trillion Events Per Day: Stream Processing in Ludicrous Mode

### Speaker(s):

  + Shrijeet Paliwal ([@shrjeet](https://twitter.com/shrijeet))

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/stream-processing-in-ludicrous-mode

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/tesla-ingestion.jpg" caption="Slide 1" >}}
{{< /gallery >}}

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

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/Kafka-as-an-event-store

### Key slides

{{< gallery caption-effect="fade" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-cqrs.jpg" caption="Slide 1" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-event-sourcing.jpg" caption="Slide 2" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-option1.jpg" caption="Slide 3" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-option2.jpg" caption="Slide 4" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-option3.jpg" caption="Slide 5" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-dual-write.jpg" caption="Slide 6" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-kafka-streams.jpg" caption="Slide 7" >}}
  {{< figure thumb="-thumb" src="/images/trivadis-summary.jpg" caption="Slide 8" >}}
{{< /gallery >}}

### Key points:

+ **normalized data leads to many joins**
+ in a DB, you store the current state, but not how it has changed over time
+ if you want to be scalable, don't rely on the DB for populating read replica(s) (e.g., write triggers, etc.)
+ [Slide 1]: CQRS
  + Command Query Responsibility Segregation
  + handle writes and reads differently/separately
+ [Slide 2]: event sourcing
  + store state-changing events, not states
+ event store
  + [Slide 3]: option 1: events per account/customer
    + always replay from offset 0)
    + not great due to the number of topics necessary (i.e., one per user)
  + [Slide 4]: option 2: events per event type (e.g., Account, Customer)
  + [Slide 5]: option 3: one topic with all events
+ [Slide 8]: Kafka alone is not a great event store
  + [Slide 7]: need a way to persist or using Kafka streams for a streaming design
+ [Slide 6]: **avoid dual writes**

---

## Streaming Ingestion of Logging Events at Airbnb

### Speaker(s):

  + Hao Wang: Senior Software Engineer, Airbnb

### Video and Slides:

+ https://www.confluent.io/kafka-summit-ny19/streaming-ingestion-of-logging-events-at-airbnb

### Key points:

  + overview of the architecture at Airbnb
  + showed some graphs
