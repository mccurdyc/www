# [`https://www.mccurdyc.dev`](https://www.mccurdyc.dev)

## Getting Started

```bash
$ git clone --recursive https://github.com/mccurdyc/www.git
$ cd www && git submodule update --init
$ make help
$ make serve
```

### Using nix-direnv

```bash
$ direnv allow
```

## Creating a New Static Asset

New static assets can be generated with the `hugo new` command and by specifying
the archetype. To read more, check out [these docs](https://gohugo.io/content-management/archetypes/#what-are-archetypes).

```bash
$ hugo new content/books/foo-bar-baz.md
$ hugo new content/posts/foo-bar-baz.md
```

## Adding Photos

```bash
hugo new content/photos/2050-foo.md
make sync-images DIR='2050/foo'
make dump-images DIR='2050/foo' >> ./content/photos/2050-foo.md
```

## Deploying

```bash
make deploy
```
