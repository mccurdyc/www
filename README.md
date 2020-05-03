# [`https://www.mccurdyc.dev`](https://www.mccurdyc.dev)

## Getting Started

```bash
$ git clone --recursive https://github.com/mccurdyc/www.git
$ cd www && git submodule update --init
$ make help
$ make serve
```

## Deploying

```bash
FASTLY_SERVICE_ID=foo FASTLY_API_KEY=bar bash -c 'make deploy'
```

## Bugs or Praise

If you find these files useful or find a bug, please let me know. I'm
@McCurdyColton on Twitter, but also feel free to open an issue here!
