---
title: "How I Read"
author: "Colton J. McCurdy"
type: ""
date: 2022-01-07
subtitle: "A tradeoff between effeciency, effectiveness and enjoyment"
image: ""
post-tags: ["reading", "2022", "hobbies", "ipad", "personal process"]
posts: ["How I Read: A tradeoff between effeciency, effectiveness and enjoyment"]
---

## Goals of reading for me

I have three goals when reading:

1. effecient referencing
2. effective retention and sharing of knowledge
3. enjoyment

My process prioritizes effeciency of "re-reads" or referring to where I learned
something and less about reading most efficiently. I don't tend to skim too often,
but I'm definitely not afraid to skim through parts in non-fiction books if I
feel something is there mostly for "fluff".

Reading for me is a balance of these three things and they do compete with each other.
The most effecient way for me to read and take notes is reading on the Kindle App
on my iPad and exporting my raw highlights to my notes, but this isn't as enjoyable
for me as a physical book. I love sniffing physical books!!!

### 850 books in a lifetime

I first started thinking about how many books I'll be able to read in my lifetime
after reading [a friend's post](https://hermanschaaf.com/how-i-choose-nonfiction-books/).
After doing a bit of rough math, I calculated that I'll probably be able to read
something like 850 books in my lifetime if I continue reading at roughly the same
pace that I do today. Here's the equation I used.

_I assumed that I would stop reading age 70 (don't ask why). 70 felt like an age
where reading maybe would be less about gaining knowledge and more for pure enjoyment
and I'd probably stop keeping track of what I read, who knows._

_yearlyConsumptionRate_1_: my current, non-retired, consumption rate which is
about 15 books.

_yearlyConsumptionRate_2_: an estimated retirement reading rate. I assumed a
book a week, so 52 books.

_((retirementAge - currentAge) * yearlyConsumptionRate_1) + ((70 - retirementAge) * yearlyConsumptionRate_2)_

_((65-26)*15))+((70-65)*52)=845_

## My process

This process is mostly for non-fiction reading. Fictional reading focuses more
on enjoyment and extrapolating themes and lessons.

### 1. Highlight

While reading a book, I will highlight things. Non-fiction books now often have
quite a bit of "fluff" to meet publisher requirements. I view highlighting as
stripping away what I consider fluff. I want to be able to re-read a book by
reading my highlights and referring back to a part of the book only if I want
more context.

In physical books, if there is a particular highlight that I don't want to miss
when writing a post for this site, I will fold the corner of the page.

### 2. Handwrite Notes

Notes for me can either be summarizations of a particular thing I've read, a
verbatim text or a thought or question that popped in my head after reading something.

I started reading non-fiction for enjoyment when I was in Detroit --- so roughly
2017. This is where I developed my process for handwritten notes. Taking physical
notes while reading books was what really helped me fall in love with reading because
I could refer to my takeaways really easy in future conversations with people.
I started by exlusively taking notes in a physical notebook with fountain pens.
This didn't change much until I purchased an iPad Air 4th generation in November
of 2020. This physical notetaking process was a very enjoyable process as I love
writing with and using fountain pens. It forces me to slow done just a bit more
as I appreciate the shading of the ink.

The iPad changed my reading process in many ways. From how I read, take and sync
notes and write these posts. The iPad is either used for highlighting in digital
books or for writing personal notes in digital form on GoodNotes 5 for physical
books. Since I mentioned GoodNotes, I'll explain why I chose that over Notability
at the time as well as other key apps for my workflow.

#### iPad Apps

##### Readwise, Readwise, READWISE!!!

Readwise has been a huge gamechanger and positive improvement in my reading process.
I use it for syncing Kindle and browser highlights to my "personal database" which
was Notion, but is now Obsidian (thanks Jon F.!). I mention Notion only to highlight
Readwise's support for exporting or syncing with Notion.

To be more specific, [this is the process](https://help.readwise.io/article/30-how-do-i-import-highlights-from-personal-documents-on-kindle)
I use to sync my Kindle highlights with Readwise. I don't refer to these synced
notes until after I've finished a book.

It's great because there is an [official Readwise-Obsidian sync plugin](https://help.readwise.io/article/125-how-does-the-readwise-to-obsidian-export-integration-work)
and it allows you to format the markdown for highlights which makes it super
efficient to then copy to a static site generator that uses markdown like Hugo
(what I use).

##### Oreilly's Safari Books Online

I use the Safari Books Online app for reading tech books. It has good support
for highlighting and exporting highlights. I make all of my highlights public
so that I can refer people to my highlights without having to export them and
upload them to my site. I don't want to rely on just making my highlights public
because they "own" my highlight data and if I decide to stop paying for a
subscription, "whoosh", highlights gone.

The process for exporting highlights isn't great. It's manual, but I haven't spent
much time focused on improving it yet. I mostly [follow this process](https://help.readwise.io/article/116-how-do-i-import-highlights-from-oreilly-learning)
for syncing to Readwise after finishing a book. I wrote a little bash script that
paginates the Oreilly highlights and downloads them to a file. However, there isn't
and official importer or sync mechanism with Readwise, so I have to email them
to `add@readwise.io`.

##### GoodNotes 5

I chose GoodNotes because I knew I was primarily going to use it for handwritten
notetaking from physical books. At the time of making the decision, GoodNotes 5
was praised for its ability to index and therefore search handwritten text.

In addition to using GoodNotes for handwritten notes, I use it for reading and
annotating PDFs. I even export Google Docs as PDFs and annotate them sometimes.

##### Obsidian

I use Obsidian for all of my personal typed note taking which I do entirely in markdown.
I could write an entire post on why I chose Obsidian. I bought pretty deep into
Notion for a while, but abadoned it mostly because I wanted to "own" my data and
due to Notion's not-quite Markdown nature. I also tried, Bear, Drafts, iAwriter,
SimpleNotes, StandardNotes and probably a few that I'm forgetting.

##### Blink.sh

I'm not going to go into too much detail in this post because I'll probably
write an entirely separate post on the topic of using my iPad for programming.
In short, it's similar to Fatih Arslan's setup that he documents [here](https://arslan.io/2019/01/07/using-the-ipad-pro-as-my-development-machine/).
That's definitely where I got the inspiration for my setup.

### 3. Post to mccurdyc.dev/books

I use Hugo as my static site generator. I try to cut as much as possible from my
highlights to get to my key takeaways from a book so that others can quickly skim
and get the gist of a book if they want.

If there is a book that I either didn't enjoy that much (usually I'll stop
reading it) or didn't have the time to invest in reducing my highlights, I'll
post my highlights verbatim.

Why don't I just publish Obsidian pages?

- I don't pay for [Obsidian's Publish feature](https://obsidian.md/publish)
- I don't want to trim my raw, exported, highlights

## What about audiobooks? Or podcasts?

To be honest, I've only briefly tried audiobooks. Because while they are
super effecient to get through a book, it's much harder to take notes because
you often aren't focused on reading when you are listening to an audiobook or podcast,
you are trying to multi-task --- whether it be while mowing, running, vacuuming,
etc. --- and as soon as I identify something I want to note down and I am trying
to keep it summarized in my head to write down, I don't focus on the rest of the
content and I get mad when I try to fumble around to write it down quickly while
mowing, etc. It just doesn't work for me right now.

For a short bit for podcasts I used [Airr](https://twitter.com/AirrAudio) because
there is a means to [sync with Readwise](https://help.readwise.io/article/103-how-do-i-save-highlights-from-the-podcasts-i-listen-to-using-airr).
I don't remember why I stopped using it other than I haven't been listening to
podcasts as much lately and because I pay for Spotify.
