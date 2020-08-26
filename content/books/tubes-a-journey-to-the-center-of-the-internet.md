---
title: "Tubes"
author: "Colton J. McCurdy"
date: 2020-08-23T09:43:58-04:00
subtitle: "A Journey to the Center of the Internet"
description: "While many people view the Internet as a bubble of omnipresent connectivity, the core of the Internet is localized to relatively few places, like Ashburn, Virginia or 60 Hudson Street in New York City. This book takes a journey to these few places that are the core to the foundation of the Internet."
cover: "tubes-60-hudson.jpg"
cover-image-title: "60 Hudson"
cover-creator-name: "Shiny Things"
cover-creator-url: "https://www.flickr.com/photos/shinythings/"
cover-source: "https://www.flickr.com/photos/shinythings/4925492711/in/photolist-8vfro8-YzwNz1-2gG4rHu-2joYoPc-2ivNqhD-286YMas-MynFqs-RtSgip-CFGrdA-2j4gEp6-4zZbwf-2hgKePZ-CCvoaN-2hg4sDu-McGsJT-kJoe3k-4zZ8pq-28FduWG-2aZoUQP-Gwxp8n-2ayHmHe-ergbtG-2gdtpSq-2jokvRT-2jxwVjd-2eiiGWk-No1LC7-GGDopJ-24NrDMS-F5vf1u-EU9PBN-2g5gQS8-CuE3ki-2haBH6J-DgfXD7-2dPSVpt-27VwXsA-srzdKZ-tXijx3-2hv2XGB-CXtfCS-r1WmjW-9jVh4U-9jSdDk-243APpg-9yx2DD-7m2Mwr-22Yf3sd-227TVCL-28be4ZE"
cover-license: "CC BY-NC 2.0"
cover-license-url: "https://creativecommons.org/licenses/by-nc/2.0/"
book-tags: ["internet", "networking", "2020"]
books: ["Tubes: A Journey to the Center of the Internet"]
book-authors: ["Andrew Blum"]
amazon: ""
thriftbooks: ""
---

While the Internet is a significant component of many people's lives, it "lives" in
locations and buildings that, relatively speaking, seem and look --- at least from
the outside --- insignificant. No signs boasting that a core piece of the
Internet lives in this building, etcetera. For example, this post's cover image is
of 60 Hudson Street, formerly known as the Western Union Building, in
the Tribeca neighborhood of Manhattan in New York City. 60 Hudson is one of, if not _the_,
single most important buildings in regards to the Internet; mostly due to its
telegraphy roots.

I read this book while on vacation in North Myrtle Beach, South Carolina. My sister,
wife and I drove the 12-or-so-hour trip through the night. To avoid going on the
windy, mountainous roads in West Virginia in the middle of the night,
we drove south-east through Pennsylvania, Maryland, Virginia and North Carolina.

It wasn't until we arrived that I started reading this book and realized that on our
route, near the Maryland-Virginia state line on interstate 495, we were within 20-miles
of Ashburn, VA, which has been referred to as ["the bullseye of America's Internet"](https://gizmodo.com/the-bullseye-of-america-s-internet-5913934).
A primary reason for this name is because it is a home to Equinix, an Internet Exchange (IX) ---
which has Internet Exchange Points (IXPs) ---, Amazon's `us-east-1` and is part of [the Dulles Technology Corridor](https://en.wikipedia.org/wiki/Dulles_Technology_Corridor).
These core pieces of the Internet reside in buildings, similar to 60 Hudson, that
probably wouldn't be worth taking a detour to see (from the outside), which is
one reason I decided that it wasn't worth taking this route on the way home.

## ~~Turtles~~ [Networks mostly with physical cables] all the way down

The "Internet" is an inter-connection of intranets. Basically, think your home network --- don't
focus on the WiFi bits ---, but a little bigger and then a bunch of those networks all over, connected
together. While we are used to using wireless networks and thinking of the Internet as
omnipresent, at probably most, if not all, levels of the Internet, there are physical wires
connecting you to the rest of the world. Yes, [even across the ocean](https://www.submarinecablemap.com/#/).
[This article from CNN](https://www.cnn.com/2019/07/25/asia/internet-undersea-cables-intl-hnk/index.html)
goes into more detail about the cable gets laid, its historical ties to telegraphy
and the possible vulnerabilities.

To me, when visualized, a network map reminds me of the human venous system, where veins
connect to other, more critical, veins and so on. Your home network
(an intranet) might be like a finger in the human venous system analogy
and connects to other parts of the body via "cross-connections".

[This fairly old post, title, "How Does the Internet Work?"](https://web.stanford.edu/class/msande91si/www-spr04/readings/week1/InternetWhitepaper.htm)
from Stanford explains it well. As you traverse up the layers of the Internet infrastructure,
specifically the hierarchy of Internet Service Providers (ISPs) --- which are just
networks, specifically intranets, themselves --- the more connections there are to the
wider Internet. At the highest level sit [Network Service Providers (NSPs)](https://broadbandnow.com/All-Providers) that
provide Internet access to your ISP, but still themselves don't possess access
to the entire Internet. The connection to the Internet as we know it is done via
cross-connections between NSPs in IXPs, like Equinix. In the book, IXPs were
described as the "translators" between ISPs (or CDNs). This is a translation of routing configurations between
entities via the Border Gateway Protocol (BGP). [The origin story for
one of the early IXPs, namely MAE-East, according to Internet architect, Steven Feldman, goes
that "A group of network providers in the Virginia area got together over beer
one night and decided to connect their networks."](https://books.google.com/books?id=8zJmxWNTxrwC&pg=PA187&lpg=PA187&dq=uunet+office+mae-east#v=onepage&q=uunet%20office%20mae-east&f=false).
I just ordered this book, so look for a future post with more details.

As a slight tangent, there was a good [On the Metal podcast episode with Kenneth Finnegan](https://oxide.computer/podcast/on-the-metal-6-kenneth-finnegan/)
where Kenneth described how as a side project, he ended up building an IXP, [namely Fremont Cabal Internet Exchange](https://blog.thelifeofkenneth.com/2018/04/creating-internet-exchange-for-even.html).

## Other Notes

I was excited to find a way to track my requests around the Internet and thankfully
Tubes introduced me to the `traceroute` Unix command.

TODO: mtr

TODO: https://twitter.com/mccurdycolton/status/1296854230184144897?s=20
@wickyvinn Deconstruct 2018 talk
