# [`https://www.mccurdyc.dev`](https://www.mccurdyc.dev)

## Getting Started

```bash
$ git clone --recursive https://github.com/mccurdyc/www.git
$ cd www && git submodule update --init
$ make help
$ make serve
```

## Creating a New Static Asset

New static assets can be generated with the `hugo new` command and by specifying
the archetype. To read more, check out [these docs](https://gohugo.io/content-management/archetypes/#what-are-archetypes).

```bash
$ hugo new books/foo-bar-baz.md
$ hugo new posts/foo-bar-baz.md
```

## Deploying

```bash
$ FASTLY_SERVICE_ID=foo FASTLY_API_KEY=bar bash -c 'make deploy'
```

## Bugs or Praise

If you find these files useful or find a bug, please let me know. I'm
@McCurdyColton on Twitter, but also feel free to open an issue here!
