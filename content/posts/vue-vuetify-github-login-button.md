---
title: GitHub OAuth Sign-in Button with Vue.js and Vuetify
description: ""
author: "Colton J. McCurdy"
date: 2019-07-10
post-tags: ["github", "vuejs", "vuetifyjs", "javascript", "naas", "2019"]
posts: ["GitHub OAuth Sign-in Button with Vue.js and Vuetify"]
image: ""
---

## NaaS: Neighbor as a Service

I'm currently working on a hosted and managed, Software as a Service (SaaS), offering
of {{< repo-link "mccurdyc/neighbor" >}} as a personal project. This SaaS offering
of neighbor is appropriately-named Neighbor as a Service or NaaS for short.
NaaS is pronounced similar to Nas or Lil Nas X, the rappers, unlike SaaS --- pronounced "sass".
The primary goal of this project is to gain experience building and marketing a
product from the ground up --- building the frontend, backend and infrastructure ---
and sharing my findings along the way.

### Choosing a Frontend Framework

The frontend framework of choice is Vue.js or Vue for short. To be honest,
the choice to use Vue instead of React was motivated by the rising popularity of Vue
and newness. React has been around longer and more people are using it.
My thought was that I wanted to share my new-found knowledge to a community
where there were fewer posts describing nuances. I definitely have found gaps in
documentation in the Vue community. I've had to scavenge around and piece various
documents and StackOverflow posts together to get the answer that I was looking for.
Another thought was that React has been around longer and has more posts written
about it and my contributions would carry less weight in that community than
they would in the Vue community.

Honestly, I didn't consider Angular because of the perceived "heaviness". My understanding
is that Angular is a full-fledged Model View Controller (MVC) framework and I was only interested in
the view piece to serve data retrieved from the backend. A more comprehensive comparison
of React and Angular can be found [here](https://programmingwithmosh.com/react/react-vs-angular/).
I am definitely not an expert in the frontend space as this is my first time working with a frontend framework
or writing frontend code for that matter, with the exception of my personal, static,
website. Most of the frontend work for my personal site was done by {{< repo-link "halogenica/beautifulhugo" >}}
and I tweaked it to fit my personal taste {{< repo-link "mccurdyc/beautifulhugo" >}}.
To read more about my personal website and theme, refer to the [site page](https://mccurdyc.dev/page/site/).

### Why Vuetify?

I wasn't searching for a material design, but I am a fan of how it looks and when
I came across Vuetify, I was "sold" --- it's free, no worries. I don't remember
how I came across/discovered Vuetify, but I do remember that the integration was
seamless. The integration with Vue was a single command `vue add vuetify`.
To read more about using Vuetify and integrating with Vue, check out the
[Quick Start page on Vuetify's website](https://vuetifyjs.com/en/getting-started/quick-start).

## GitHub OAuth Sign-in Button or `v-btn` in Vuetify

<p align="center">
  <img src="/images/naas-toolbar.png">
</p>

Due to the nature of neighbor, signing in to GitHub to access resources is necessary.
Alternatively, we could have accepted a [GitHub personal access token](https://help.github.com/en/articles/creating-a-personal-access-token-for-the-command-line),
but this seems like an unfamiliar alternative to signing in with GitHub on the web.
Conversely, at the command-line or cli, redirecting to GitHub in your browser to sign
is a poor cli experience as it interrupts the flow every time you run a command.

GitHub does provide a [great document](https://developer.github.com/v3/guides/basics-of-authentication/)
outlining the process for setting up authentication. Below, is one of the code snippets
from the document, where you see the URL that you are supposed to use to make
the authentication request to GitHub's API. As advised by GitHub, "you should never,
ever store these values in GitHub--or any other public place". They suggest using
environment variables, which is what I will demonstrate below.

<br/>
```html
<a href="https://github.com/login/oauth/authorize?scope=user:email&client_id=<%= client_id %>">Click here</a> to begin!</a>
```

<br/>
While it isn't much different from using an `<a>` tag in HTML, there are some
nuances that caused me to spend more time than I originally thought it would take
to get this working in Vue with a Vuetify `v-btn`.

First, create a `v-btn`. You can see what the button looks like on my website in
the above image. The important pieces are the `v-bind` and `link.url`. `v-bind`
is necessary for using data from Vue. I found that I couldn't do string concatenation
directly using an environment variable in the `href` field and instead had to use
Vue data, which brings us to the second important piece, `link.url`. The name isn't
important as this is just what I decided to name it. I define `link.url` in the
`<script>` section of the Vue file under the `data` field as an object named `link`,
with a field, `url`. In the `<script>` section, we can write JavaScript, so leveraging
[template literals or template strings](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals)
is possible. Similarly, accessing an environment variable here is done using `process.env.*`.

<br/>
```html
<v-btn v-bind:href="link.url">
  <font-awesome-icon class="fa-fw" :icon="['fab', 'github']"/>
  Sign In With GitHub
</v-btn>
```

<br/>
One important note regarding [environment variables in Vue](https://cli.vuejs.org/guide/mode-and-env.html#using-env-variables-in-client-side-code)
though is that in client-side code, environment variables must be prepended with `VUE_APP_`.
Along with the official Vue documentation for accessing environment variables, I
found [this post](https://alligator.io/vuejs/working-with-environment-variables/)
helpful.

Note: `v-bind:href="link.url"` can be shortened to `:href="link.url"` as seen in [this
StackOverflow post](https://stackoverflow.com/questions/40899532/how-to-pass-a-value-from-vue-data-to-href).

<br/>
```html
<script>
export default {
  name: 'App',
  app_icon: 'arrow-right',
  data: () => ({
    link: {
      url:`https://github.com/login/oauth/authorize?scope=user:email&client_id=${process.env.VUE_APP_GITHUB_CLIENT_ID}`
    }
  })
}
</script>
```
