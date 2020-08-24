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

While the Internet is a significant portion of many people's lives, it "lives" in
places and buildings that relatively speaking seem and look --- at least from
the outside --- insignificant. No signs boasting that a core piece of the
Internet lives in this building, etc..

I read this book while on vacation in North Myrtle Beach, South Carolina. My sister,
wife and I drove the 12-or-so-hour trip through the night. To avoid going on the
windy roads through the mountains in West Virginia in the middle of the night,
we drove south-east through Pennsylvania, Maryland, Virginia and North Carolina. It wasn't until we
had arrived that I started reading this book and realized that where we drove through
near the Maryland-Virginia state line on interstate 495, was only
about 10-miles from the nation's capitol. More importantly as this route relates to the book, we
were about 20-miles south-east of Ashburn, VA, which is ["... the bullseye of America's Internet"](https://gizmodo.com/the-bullseye-of-america-s-internet-5913934)
because this is where via Equinix's --- an Internet Exchange Point (IX) --- cross-connects,
intranets connect.

## ~~Turtles~~  Networks with cables all the way down

The "Internet" is an inter-connection of intranets. Basically, think your home network,
but a little bigger and then a bunch of those networks all over, connected
together. While we are used to using wireless network and thinking of the Internet as
omnipresent, at probably every level of the Internet, _except_ your home wireless
or LTE, there are physical wires connecting you to the rest of the world.

When visualized, to me, reminds me of the human venous system, where veins
connect to other, more critical, veins and so on. Except in the Internet, there is no central "heart" (this is actually a good thing!).
Your home network (an intranet) might be like a finger in the human venous system analogy
and connects to other parts of the body via interconnections.

[This fairly old post, title, "How Does the Internet Work?"](https://web.stanford.edu/class/msande91si/www-spr04/readings/week1/InternetWhitepaper.htm)
from Stanford explains it well. As you traverse up the layers of the Internet infrastructure,
specifically the hierarchy of Internet Service Providers (ISPs) --- which are just
networks themselves --- the more connections there are to the
wider Internet, up to the highest level of connections which are ISPs with
nation-wide _intranet_ visibility. However, while these NSPs have nation-wide scope
_in their own network --- i.e., intranet ---_, they need to use an IX to access
other nation-wide ISPs' intranets. In the book, the IXs were described as "translators"
between ISPs.

As a slight tangent, there was a good [On the Metal podcast episode with Kenneth Finnegan](https://oxide.computer/podcast/on-the-metal-6-kenneth-finnegan/)
where Kenneth described how as a side project, he ended up building an IX, [namely Fremont Cabal Internet Exchange](https://blog.thelifeofkenneth.com/2018/04/creating-internet-exchange-for-even.html).

## Other Notes

I was excited to find a way to track my requests around the Internet and thankfully
Tubes introduced me to the `traceroute` Unix command.

TODO: mtr

TODO: https://twitter.com/mccurdycolton/status/1296854230184144897?s=20
@wickyvinn Deconstruct 2018 talk
