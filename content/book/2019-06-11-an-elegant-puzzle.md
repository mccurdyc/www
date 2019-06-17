---
title: "An Elegant Puzzle"
subtitle: "Systems of Engineering Management"
author: "Colton J. McCurdy"
date: 2019-06-11
abstract: "\"An organization is a collection of people working toward a shared goal.\" Yet, it is often a challenge getting people to \"gel\" and have everyone work optimally together. This book talks proposes ideas that worked (or didn't work) for the author in his career managing engineers."
book-tags: ["book", "2019"]
books: ["An Elegant Puzzle: Systems of Engineering Management"]
book-authors: ["Will Larson"]
---

> ...management, at its core, is an ethical profession.

<br/>

---

## Do What is Best for the Company

> An organization is a collection of people working toward a shared goal.

Personally, this took me about a year in industry to really grasp the idea that
I can't always do the ideal Engineering things e.g., pay technical debt until I
feel comfortable with a system. The relationship between Product and Engineering
is very much a balancing act and if the pendulum is swung too far in either direction,
then we aren't doing what is best of our users or ourselves.
Even if we are delivering new features all of the time,
if our site is slow or unreliable, users will overlook features unable to use
them if the site is completely down. But as engineers, we also have
to keep in mind that without a product, there is no Engineering team.

What I've found works really well is when Product and Engineering are listening
and looking out for each other. There is one person in particular on Product
who I work with who used to be an engineer and knows when and when they cannot push for
features. From the other side, more recently with knowledge
instilled by my manager, I've been encouraging others to do things that "don't scale"
until we get a good mental model of the problem and ultimately establish
product/market fit. Rather than designing and building _what_ we think the
solution is without experiencing the problem and its nuances. The ultimate goal
is to do what is best for the company and its users.

## Engineering Teams

Part of being an effective Engineering organization is establishing strong relationships
with each other, between teams and with the pieces of the system that we own. This
can be achieved in part by properly designing teams.

### Team Sizing

> "this might be the best book I have ever read on engineering teams" and by page 42 I knew for sure. -[@mipsytipsy](https://twitter.com/mipsytipsy)

The foundation of properly-designed teams is correct size --- not too big or small.
Will proposes that engineering managers should manage six to eight engineers. Any
smaller than six to eight engineers, managers are getting too deep into technical
pieces --- e.g., designing systems, etc. --- and less focused on the people side of the
job. However, managing more than eight leads to managers becoming solely "safety nets".

In regards to managers of managers, or "second-degree" managers, Will suggests
that second-degree managers should manage four to six managers. Again, fewer
than this number leads to feeling underutilized and getting too deep in solving
others' problems and more than this leads to "coaching".

In my experience, when the team is too large and owns a wide range of systems or
parts of a single, larger system, it leads to engineers "tuning out" during _regular_ team
ceremonies when others are talking about their part. It can be helpful
to give or receive feedback on other parts of the system, but not in _regular_
meetings. Also, naturally large teams lead to inner-, "micro"-, teams forming
in order to be effective owners of part(s) of a system. If these micro-teams don't
form, then the range of tasks that one picks up is very large, leading to lack
of ownership of systems and ultimately weak standards and poor quality. It's also
harder when there has been a clear owner of a system and _many_ other members of
the larger team are "visiting" the project, doing one task and then not contributing
to the project for a long period of time. This results in paying the cost of
on-boarding individuals, frequently, or in this case basically for every task.

### Getting to the Proper Size

Will names four sources --- that are "probably in order" --- of candidates for staffing a team:

1. Team members who are ready to fill the role now
2. Team members who will grow into the role
3. Internal transfers
  + Will does suggest later that internal transfers are very costly due to disrupting the "gelling" process.
4. External hires who are ready to fill the role now

### Four States of a Team

There are four states of a team, in order.

1. Falling behind
2. Treading water
3. Repaying debt
4. Innovating

#### Falling Behind

Will defines falling behind as the team's backlog of tasks continuing to grow at
a rate greater than the rate at which the team pulls tasks from their backlog.
Eventually, the backlog will become so large that tasks will become "non-issues"
just due to how systems change, which means that the backlog will be polluted.

One way to address falling behind is to grow the team to adequately support the product
for which they are responsible for building features and fixing bugs. You can't
tell the Product team to stop thinking of ways to better the Product or solve
user problems. This is not an option. You can however, work with Product to properly
prioritize and set expectations of delivery date. This still doesn't solve being
able to deliver multiple pieces that are critical to get out in a timely fashion
when you don't physically have enough engineering resources.

#### Treading Water

Pulling from the backlog at the same rate as tasks are added is what Will defines
as "treading water". This often means that in order to address technical debt, fixes
need to be incorporated into Product features rather than specifically addressing technical debt.

Will suggests one way of addressing the lack of forward momentum is to focus on
finishing and reduce on-going, concurrent work.

#### Repaying Debt

I view this as the opposite of treading water where instead of fixing technical debt
by incorporating fixes into features, features are integrated into addressing
technical debt changes.

#### Innovating

This is the point where the team truly starts thinking outside of the box, potentially
doing things that are novel to the industry. But Will makes it clear that during
this phase of a team, it is important that the team doesn't get labeled as the
team that "builds science projects".

### Managing Engineering Reorganizations

Reorganizations are mentioned in [The Hard Things About Hard Things](https://www.amazon.com/Hard-Thing-About-Things-Building/dp/0062273205/ref=asc_df_0062273205/?tag=hyprod-20&linkCode=df0&hvadid=312106851030&hvpos=1o1&hvnetw=g&hvrand=10572678781748792168&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9006368&hvtargid=pla-423142296641&psc=1)
also, where author, Ben Horowitz, says, that it is crucial to nail the structure
down with a small group of people and then to roll it out quickly and clearly.

Successful reorganizations can be challenging and risky, motivating Will's point
that one of the best types of reorganizations that you can do is the "one that
you don't do".

Two best types of reorgs.

1. one that solves a structural problem
2. one that you don't do

<br/>

While there are two _best_ types of reorgs., there is only one type of worst reorg.
The worst type of reorganization is the one that you do to avoid a people management
problem (e.g., two employees who often argue). Will actually suggests to solve
people problems, putting these people closer together
as to reduce people or communication barriers between them.

## "Model, Document, Share"

> ...in [Will's] experience, [Model, Document, Share] has lead to more adoption than top-down mandates have.

This is basically the idea of collecting metrics to establish a baseline, making
small changes and tweaking until it is "successful". Then, you
document why it was successful. Next, get a _few_ people from other teams to
confirm that the approach is effective given the same, or similar, problem. Finally, _sharing_
the approach **not** lobbying for everyone to adopt the approach.

I have recently adopted this as my approach to sharing my solution to a problem.
Similar to Will, I have experienced wider adoption than me lobbying for the change.
In a later section title, Communities of Learning, Will mentions that a key point
in getting the wider community to contribute is to "be a facilitator, not a lecturer".
I think this point is also applicable in sharing what you have found to be effective.

## Positive and Negative Freedoms

> A positive freedom is the freedom _to_ do something... A negative freedom is the freedom _from_ things...

In my experience as an engineer, these freedoms --- positive and negative --- are
what have made working with a manager a good or poor experience. Organization structure
did also play a part as in the poor experience as my manager was not able to keep the
team free _from_ stakeholders coming directly to us individual contributors with
requests and demanding updates. One manager empowered everyone to, or gave us
the freedom _to_, design and think freely about solutions to problems rather than
telling us their solution or tool for the job.

## Work the Policy; Not the Exceptions

Working the policy instead of the exceptions, means don't make the one-off exceptions.
Instead, frequently evaluate the policy that is in place and change as you see
fit _during the evaluation period_, not when presented with an exception. Basically,
give things a chance to prove effective or ineffective before changing them.

## Career Ladder

The infamous "ladder", while it may seem unimportant, is actually a huge part of
establishing a successful culture. The ladder helps set expectations and define
role models.

> A good ladder allows individuals to accurately self-access... A bad ladder is ambiguous and requires deep knowledge of precedent to apply correctly.

Will further stresses the importance of the career ladder when he says,

> If there is one component of performance management that you are going to invest in doing well, make it the ladders: everything else builds on this foundation.

## Presenting to Leadership

I've failed at presenting to many leaders before, not presenting few, clear goals
or action items, but instead listing _everything_ that I felt needed considered.
Instead, as Will suggests, I should have presented a few points very clearly.

Will provides a few additional points on the topic of engaging leadership:

* Communication is company-specific
* Start with the conclusion
* Frame _why_ the topic matters to the company; not just to yourself
* Everyone loves a narrative
    * "where things are now, how you got here and where you're going now"
* Prepare for detours
* Prepare a lot; practice a little
    * Basically, be prepared for detours rather than word-for-word what you are going to say.

In order, your pitch should go as follows:

1. Tie the topic to business value
2. The historical narrative
3. Explicit ask
4. Data-driven diagnosis
5. How did you make the decision
6. What's next and when will it be done
7. Return to the explicit ask

---

# Appendix

## Individual Contributors Should Still Understand Management

{{<tweet 1135881974424358913>}}

> Every engineer should read this.  Not just managers.

Before Charity Majors posted that Tweet, I posted a Tweet making a similar statement.
The other books included in the picture are of a similar genre to An Elegant Puzzle.
This "self-help" genre is one that I most frequently read.

{{<tweet 1134086064514187264>}}

Reading these books enables me to be a knowledgable contributor in the challenging
problems that exist at a fast-growing company. These books have also helped prepare
me for one-on-ones with people at the highest level in the company and frequent
one-on-ones with my manager and managers two and three levels above me.

In the Appendix of An Elegant Puzzle, Will lists books and papers that have been
helpful in his career. One in particular that stood out to me was [The Mythical Man-Month](https://www.amazon.com/Mythical-Man-Month-Software-Engineering-Anniversary/dp/0201835959).
More specifically, it was Will's note about why this book was impactful for him.
Will mentioned that this was the first professional book that he had ever read
and that it "opened [his] eyes to the wealth of software engineering literature
waiting out there". The Mythical Man-Month was part of my college Computer Science
curriculum and I have revisited it a few time since. This book had a similar
impact for me i.e., introducing me to a genre of literature that is extremely useful
in my day-to-day life as a software engineer in industry. As shown below in my Tweets,
many of my challenges as a software engineer are not purely technical.

{{<tweet 1138075343552688128>}}

{{<tweet 1138436722600140801>}}
