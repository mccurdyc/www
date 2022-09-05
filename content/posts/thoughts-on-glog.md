---
title: Should I Use golang/glog?
description: ""
author: "Colton J. McCurdy"
date: 2019-05-03
post-tags: ["glog", "logging", "neighbor", "2019"]
posts: ["Should I Use golang/glog"]
---

## Background and Problem Definition

I am currently working on an open source cli tool, namely {{< repo-link "mccurdyc/neighbor" >}},
that concurrently clones and executes an arbitrary binary on the repositories returned
from a GitHub search query. This tool aims to assist both developers in academia
when collecting projects for analyses and those in industry for automating redundant
tasks e.g., adding a CODEOWNERS or LICENSE file to all of an organization's repositories.

### Why is logging important for neighbor?

neighbor executes an arbitrary binary, specified by the user e.g., `ls -al`. Therefore,
neighbor cannot be prescriptive in it's output format e.g., a CSV file with the "results".
But instead, the output is specified by the executed binary. The logs are the
focal point for a user interacting with neighbor. neighbor also aims to not be
restrictive e.g., only writing to a file, but rather flexible, in regards to the
output format. If a user wants to write to a file, they can still do so by redirecting
output streams --- both stdout and stderr --- to files, even separate files
with [the Unix redirection operator `>`](http://homepages.uc.edu/~thomam/Intro_Unix_Text/IO_Redir_Pipes.html).
This is why the logging library that is used by neighbor is important.

Example:

```bash
neighbor --query="org:neighbor-projects NOT minikube" \
         --external_command="ls -al" \
         > out.log 2>error.log
```

Originally, neighbor used {{< repo-link "sirupsen/logrus" >}}, which would allow
a user to specify log severity levels --- debug, info, warning, error, etc. --- through
an environment variable, `LOG_LEVEL`. logrus also provides the ability for structured
logging, which actually wasn't necessary for this tool. Similar to many logging
libraries, logrus provides too many unnecessary features for neighbor. logrus is
a great logging library and I actually default to using it when building servers
in Go.

One reason that I wanted to move away from logrus was because I didn't want a user
to have to be concerned about which logs were debug and which were info or error,
but instead only specify whether they wanted more or less verbosity. Admittedly,
neighbor could output all of its logs as debug-level (or error-level where necessary),
while the binary's logs are info-level and maybe this is something that I later
decide to revert back to, but I'm also interested in gaining experience with other
logging libraries. I think that this concern can be combatted by providing an
explicit definition of the `N` verbosity levels, similar to what kubectl has
done (shown below).

## Finding neighbor's future logging library

Having used `kubectl`, I wanted to have similar [verbosity-level logging interface](https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-output-verbosity-and-debugging)
i.e., `-v=N`, available via cli flags rather than an environment variable. Admittedly, I
could have exposed and parsed my own `-v` flag and set the logrus log level based
on that.

![](/images/kubectl-verbosity-logging.png)

After checking out log libraries, I actually expected to find that kubectl was
using {{< repo-link "golang/glog" >}}, but instead when I
[searched the Kubernetes repository on GitHub for "golang/glog"](https://github.com/kubernetes/kubernetes/search?q="golang%2Fglog"&unscoped_q="golang%2Fglog")
there were only two pages of results, none of which were what I was looking for.
I continued my search for the library used and that is when I came across a discussion
in [Issue#61006](https://github.com/kubernetes/kubernetes/issues/61006) where [it
was stated](https://github.com/kubernetes/kubernetes/issues/61006#issuecomment-437606019)
that the main Kubernetes repository was using {{< repo-link "k8s.io/klog" >}}, a
drop-in replacement for golang/glog that could safely co-exist and addressed
major issues faced in the Kubernetes project. The primary issue with golang/glog
was that it is no longer under active development and the Kubernetes project wanted
to have more control over the log library and that is when they decided to fork the golang/glog
project. A few other generally applicable issues to those using golang/glog outside
of Kubernetes are as follows:

1. Initializing "hidden" global flags in `init()`
2. If golang/glog fails to write, it calls `os.Exit`

The first point is a major issue if you are creating a library that will be used
by others because now, you have "infected" all consumers and transitive consumers
of your library with these flags and the consumer project will have to call
`flag.Parse()` in `init()` to register the flags. The second point, if glog
fails to write, `os.Exit` is called. Again, this is actually acceptable behavior
for neighbor because logs are the primary interface for the user and the binary run.

Prior to my investigation, I did recall seeing a few [tweets from Peter Bourgon](https://twitter.com/search?q=from%3Apeterbourgon%20glog&src=typd),
where glog was strongly advised against being used.

{{< tweet user="mccurdyc" id="972177627996831744" >}}

After seeing people pointing out the challenges of using glog, I expected to run
into a few myself. A couple of resources that I came across once I had decided to use
glog were [this blog post](https://flowerinthenight.com/blog/2017/12/01/golang-cobra-glog)
and [this GitHub gist](https://gist.github.com/heatxsink/7221ebe499b0767d4784).
Both of these resources display the usage in code with only a single, main package,
but did effectively display the use of `flag.Parse()` before logging.

Right now, I am happy with results and there is a limited set of users. If neighbor
gains traction and users would like a different interface to the logs, this will
be something that I will consider. At the end of the day, neighbor is a small project
and swapping the logging library used is relatively easy. If nothing else, it
will be a learning experience with a new (for me) logging library.

I'm curious to hear your thoughts, here is a Twitter thread where I've started
the discussion.

{{< tweet user="mccurdyc" id="1123729020145799170" >}}
