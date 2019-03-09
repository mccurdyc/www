---
title: Site
comments: false
---

# View The Source

{{< repo-link "mccurdyc/www" >}}

---

# Colorscheme
{{< partial "hero" >}}

<br>
#### Source

{{< repo-link "mccurdyc/beautifulhugo/blob/master/static/css/main.css" >}}

```css
:root {
  --base00: #2d2d2d;
  --base01: #393939;
  --base02: #515151;
  --base03: #747369;
  --base04: #a09f93;
  --base05: #d3d0c8;
  --base06: #e8e6df;
  --base07: #f2f0ec;
  --base08: #f2777a;
  --base09: #f99157;
  --base0a: #ffcc66;
  --base0b: #99cc99;
  --base0c: #66cccc;
  --base0d: #6699cc;
  --base0e: #cc99cc;
  --base0f: #d27b53;
}

.base00 { color: var(--base00); }
.base01 { color: var(--base01); }
.base02 { color: var(--base02); }
.base03 { color: var(--base03); }
.base04 { color: var(--base04); }
.base05 { color: var(--base05); }
.base06 { color: var(--base06); }
.base07 { color: var(--base07); }
.base08 { color: var(--base08); }
.base09 { color: var(--base09); }
.base0a { color: var(--base0a); }
.base0b { color: var(--base0b); }
.base0c { color: var(--base0c); }
.base0d { color: var(--base0d); }
.base0e { color: var(--base0e); }
.base0f { color: var(--base0f); }
```

#### Inspiration

{{< repo-link "htdvisser/hugo-base16-theme" >}}

---

# Site Theme

This is a customized port of [Beautiful Hugo](https://github.com/halogenica/beautifulhugo), which is a port of the Jekyll theme
[Beautiful Jekyll](https://deanattali.com/beautiful-jekyll/) by [Dean Attali](https://deanattali.com/). It supports most of the features of the original theme.

<br>

{{< repo-link "mccurdyc/beautifulhugo" >}}

### Using the theme

1. [Start a Hugo project](https://gohugo.io/getting-started/quick-start/)
```bash
hugo new site your-site-name
```
2. Initialized the Git Repository
```bash
git init
```
3. "Install" the theme
```bash
git submodule add https://github.com/mccurdyc/beautifulhugo.git themes/beautifulhugo
```

4. [Update your config.* to use the theme](https://gohugo.io/themes/installing-and-using-themes/) (if using `toml` add the following)
```toml
themesDir = "themes"
theme = "beautifulhugo"
```

Original: {{< repo-link "halogenica/beautifulhugo" >}}

![Beautiful Hugo](/images/og-screenshot.png)
