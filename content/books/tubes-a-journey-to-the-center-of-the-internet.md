---
title: "Tubes"
author: "Colton J. McCurdy"
date: 2020-08-23T09:43:58-04:00
subtitle: "A Journey to the Center of the Internet"
description: "While the Internet may feel like a bubble of omnipresent connectivity, the core of the Internet is localized to relatively few places; like Ashburn, Virginia or 60 Hudson Street in New York City. This book takes a journey to these few places that are the foundation of the Internet."
image: "/images/tubes-a-journey-to-the-center-of-the-internet/cover.jpg"
book-tags: ["internet", "networking", "2020"]
books: ["Tubes: A Journey to the Center of the Internet"]
book-authors: ["Andrew Blum"]
amazon: "https://www.amazon.com/Tubes-Journey-Internet-Andrew-Blum/dp/0061994952"
thriftbooks: "https://www.thriftbooks.com/w/tubes-a-journey-to-the-center-of-the-internet_andrew--blum/323183/item/40202917/?mkwid=3KrTPiKg%7cdc&pcrid=11558858306&pkw=&pmt=be&slid=&product=40202917&plc=&pgrid=3970769380&ptaid=pla-1101002865068&utm_source=bing&utm_medium=cpc&utm_campaign=Bing+Shopping+%7c+Computers+&+Technology&utm_term=&utm_content=3KrTPiKg%7cdc%7cpcrid%7c11558858306%7cpkw%7c%7cpmt%7cbe%7cproduct%7c40202917%7cslid%7c%7cpgrid%7c3970769380%7cptaid%7cpla-1101002865068%7c&msclkid=4282c3af30ca1757f73a9ce8ad9dbb06#isbn=0061994936&idiq=40202917"
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
A primary reason for this name is because it is a home to one of the largest Internet Exchanges (IX),
namely Equinix, Amazon's `us-east-1` and is part of [the Dulles Technology Corridor](https://en.wikipedia.org/wiki/Dulles_Technology_Corridor).
These core pieces of the Internet reside in buildings, similar to 60 Hudson, that
probably wouldn't be worth taking a detour to see (from the outside); this is
one reason I decided that it wasn't worth taking this route on the way home.

## ~~Turtles~~ [Networks mostly with physical cables] all the way down

The "Internet" is an inter-connection of intranets. Basically, think your home network --- don't
focus on the WiFi bits --- but quite a bit bigger and then a bunch of those networks all over, connected
together. While we are used to using wireless networks and thinking of the Internet as
omnipresent, at probably most, if not every, level of the Internet, there are physical wires
connecting you to the rest of the world. Yes, [even across the ocean](https://www.submarinecablemap.com/#/).
[This article from CNN](https://www.cnn.com/2019/07/25/asia/internet-undersea-cables-intl-hnk/index.html)
goes into more detail about the cable laying process, its historical ties to telegraphy
and the possible vulnerabilities.

To me, when visualized, a network map reminds me of the human venous system; where veins
connect to other, more critical, veins and so on. Your home network
(an intranet) might be like a finger in the human venous system analogy
and connects to other parts of the body via "cross-connections" at an Internet Exchange
Point (IXP).

[This fairly old post, title, "How Does the Internet Work?"](https://web.stanford.edu/class/msande91si/www-spr04/readings/week1/InternetWhitepaper.htm)
from Stanford explains it well. As you traverse up the layers of the Internet infrastructure,
specifically the hierarchy of Internet Service Providers (ISPs) --- which are just
networks --- the more connections there are to the
wider Internet. At the highest level sit [Network Service Providers (NSPs)](https://broadbandnow.com/All-Providers)
which are cross-ISP connections.

In the book, IXPs were described as the
"translators" between ISPs.
This is a translation of routing configurations between entities via the
Border Gateway Protocol (BGP). The origin story for
one of the early IXPs, namely MAE-East, according to Internet architect, Steven Feldman, in [The Shadow Factory](https://books.google.com/books?id=8zJmxWNTxrwC&pg=PA187&lpg=PA187&dq=uunet+office+mae-east#v=onepage&q=uunet%20office%20mae-east&f=false)
is that ["A group of network providers in the Virginia area got together over beer
one night and decided to connect their networks"](https://books.google.com/books?id=8zJmxWNTxrwC&pg=PA187&lpg=PA187&dq=uunet+office+mae-east#v=onepage&q=uunet%20office%20mae-east&f=false).
I just ordered The Shadow Factory, so look for a future post with more details.

Related, there is a good [On the Metal podcast episode with Kenneth Finnegan](https://oxide.computer/podcast/on-the-metal-6-kenneth-finnegan/).
In the episode, Kenneth described how, as a side project, him and a group of friends ended
up building an IXP, [namely Fremont Cabal Internet Exchange](https://fcix.net/).
Kenneth has a [post](https://blog.thelifeofkenneth.com/2018/04/creating-internet-exchange-for-even.html)
describing why they ended up doing this. In [another post](https://blog.thelifeofkenneth.com/2017/11/creating-autonomous-system-for-fun-and.html)
by Kenneth, he goes into more detail about what ISPs do; which mainly consists of possessing
a large public IP address space and routing between other ISPs address spaces via
BGP on an Autonomous System and also peering. According to Kenneth, peering often
involves backroom handshakes between humans.

At least in my understanding, peering with multiple Autonomous Systems is what makes the Internet reliable. If
one Autonomous System is failing, another will still be able to route traffic to
the desired destination.
[I tweeted](https://twitter.com/mccurdycolton/status/1296854230184144897?s=20)
a link to a talk at [Deconstruct '18](https://www.deconstructconf.com/2018),
by [vicky nguyen](https://twitter.com/wickyvinn) who goes into detail about routing,
finding the fastest routes and more!

After reading this book, I was excited to see the routes my requests took around
the Internet. Thankfully, the book did mention a Unix tool for doing just this, namely
`traceroute`. I messed with `traceroute` a bit and then a colleague introduced
me to `mtr`, which I've found nicer to use.
