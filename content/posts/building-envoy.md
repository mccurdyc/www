---
title: "Building Envoy from Source"
description: 'This post could alternatively been called "how I learn something completely new with only minimal awareness of the adjacent tooling, but really (well kinda) wanting to do a thing; An unedited process of learning and thoughts"'
author: ""
date: 2025-06-15T20:52:23-04:00
subtitle: ""
image: ""
post-tags: ["envoy", "2025"]
posts: ["Building Envoy"]
draft: false
---

This post could alternatively been called "how I learn something completely new with only minimal awareness of the adjacent tooling, but really (well kinda) wanting to do a thing; An unedited process of learning and thoughts"

# Motivation

I wanted to build Envoy with the wasmtime WASM runtime and nixpkgs envoy package errors when you add `wasmRuntime="wasmtime"` and I wanted to submit a patch to fix. But while I know Nix fairly well, I'm no expert. Also, I've never written C++, nor have I ever used Bazel. Prior to this my knowledge of Bazel was that it was Google and it was a build system.

To be honest, I wasn't even that motivated to make this work, because just using the Docker image that had Envoy compiled with WASM would have got me what I wanted. I honestly don't know why I dug in. Maybe because I do want to contribute to Envoy and understand the WASM parts of Envoy.

It was kind of out of spite that NixOS told me "you should know this" and this felt like a good deep dive. And then, once I got invested enough, then it became an opportunity for me to capture my full thought process of trying something.

Then, this became a personal challenge of "so you think you are smart and know how to learn, prove it".
You tell yourself this, but how often do you really prove it.

# Manually Building Envoy

https://github.com/envoyproxy/envoy/tree/main/bazel#production-environments
```bash
bazel build -c opt envoy
...
The current `lockfile` is out of date for 'dynamic_modules_rust_sdk_crate_index'. Please re-run bazel using `CARGO_BAZEL_REPIN=true` if this is expected and the lockfile should be updated.
```

```bash
CARGO_BAZEL_REPIN=true bazel build -c opt envoy
...
ERROR: Error computing the main repository mapping: no such package '@@dynamic_modules_rust_sdk_crate_index//': Command [/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel, "splice", "--output-dir", /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/splicing-output, "--splicing-manifest", /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/splicing_manifest.json, "--config", /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel.json, "--cargo", /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/bin/cargo, "--rustc", /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/bin/rustc, "--cargo-lockfile", /home/mccurdyc/src/github.com/mccurdyc/envoy/source/extensions/dynamic_modules/sdk/rust/Cargo.lock, "--nonhermetic-root-bazel-workspace-dir", /home/mccurdyc/src/github.com/mccurdyc/envoy] failed with exit code 127.STDOUT ------------------------------------------------------------------------
STDERR ------------------------------------------------------------------------
Could not start dynamically linked executable: /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazelNixOS cannot run dynamically linked executables intended for genericlinux environments out of the box. For more information, see:
https://nix.dev/permalink/stub-ld
```

So I knew this was related to NixOS not preferring to run dynamically-linked executables. I didn't want to make it "just work" by allowing it to use dynamically-linked executables. 

The error message told me this was related to this path `envoy/source/extensions/dynamic_modules/sdk/rust/` so let's change to this directory and try to manually build this. I see a `BUILD` file, so let's try using `bazel build`

```bash
CARGO_BAZEL_REPIN=true bazel build
...
Could not start dynamically linked executable: /home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel
```

Seems like it wants `cargo-bazel` which appears to be in nixpkgs and I just did a grep for `dynamic_modules_rust_sdk_crate_index` and found [this](https://github.com/mccurdyc/envoy/blob/c01676e090c94fe4ee720534146a4f177931530d/bazel/dependency_imports.bzl#L217-L223).
```python
# bazel/dependency_imports.bzl
def crates_repositories():
    crates_repository(
        name = "dynamic_modules_rust_sdk_crate_index",
        cargo_lockfile = "@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.lock",
        lockfile = Label("@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.Bazel.lock"),
        manifests = ["@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.toml"],
    )
```

So I changed to the `source/extensions/dynamic_modules/sdk/rust` directory to look at the `Cargo.toml` file and since this looks like a valid rust package, why not just try `cargo build`.

```bash
cargo build
...

  --- stderr

  thread 'main' panicked at /home/mccurdyc/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/bindgen-0.70.1/lib.rs:622:27:
  Unable to find libclang: "couldn't find any valid shared libraries matching: ['libclang.so', 'libclang-*.so', 'libclang.so.*', 'libclang-*.so.*'], set the `LIBCLANG_PATH` environment variable to a path where one of these files can be found (invalid: [])"
```

```bash
nix shell 'nixpkgs#libclang'

find /nix/store -name "libclang.so*"
/nix/store/4xqa6mk1lllnsprl2swlw94vczzn02y9-clang-19.1.7-lib/lib/libclang.so.19.1.7
/nix/store/4xqa6mk1lllnsprl2swlw94vczzn02y9-clang-19.1.7-lib/lib/libclang.so
/nix/store/4xqa6mk1lllnsprl2swlw94vczzn02y9-clang-19.1.7-lib/lib/libclang.so.19.1

RUST_BACKTRACE=full LIBCLANG_PATH=/nix/store/4xqa6mk1lllnsprl2swlw94vczzn02y9-clang-19.1.7-lib/lib/ cargo build
  ./../../abi.h:43:10: fatal error: 'stdbool.h' file not found 

  thread 'main' panicked at build.rs:29:6:
  Unable to generate bindings: ClangDiagnostic("./../../abi.h:43:10: fatal error: 'stdbool.h' file not found\n")
```

```nix
pkgs.mkShell {
  buildInputs = [
    pkgs.cargo
    pkgs.rustc
    pkgs.clang
    pkgs.libclang
    pkgs.stdenv.cc
  ];
  LIBCLANG_PATH = "${pkgs.libclang.lib}/lib";
  BINDGEN_EXTRA_CLANG_ARGS = "--include-directory=${pkgs.stdenv.cc.libc.dev}/include";
}
# okay now this builds with `cargo build`
```

```bash
CARGO_BAZEL_REPIN=true bazel build
# same error
```

Oh, let's try clearing the Bazel cache `rm -rf ~/.cache/bazel`. Nope. What if we "just" add `cargo-bazel` to our shell? Nope.

Where is `cargo-bazel` referenced in the project? Nowhere...

Okay, what is "cargo-bazel" then "`cargo-bazel` is a Bazel repository rule for generating Rust targets using Cargo." Which links to https://github.com/abrisco/cargo-bazel, but this is deprecated and redirects to "This project has been upstreamed into [bazelbuild/rules_rust](https://github.com/bazelbuild/rules_rust) as the [crate_universe](https://bazelbuild.github.io/rules_rust/crate_universe.html) package. This repository is archived and development for the project will continue in the `rules_rust` repository."

Okay, I know I've see `rules_rust` in the project, let's grep again. Okay I come across [this](https://github.com/mccurdyc/envoy/blob/c01676e090c94fe4ee720534146a4f177931530d/bazel/repository_locations.bzl#L1459-L1474)

```bash
    # After updating you may need to run:
    #
    #     CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index
    #
    rules_rust = dict(
        project_name = "Bazel rust rules",
        project_desc = "Bazel rust rules (used by Wasm)",
        project_url = "https://github.com/bazelbuild/rules_rust",
        version = "0.56.0",
        sha256 = "f1306aac0b258b790df01ad9abc6abb0df0b65416c74b4ef27f4aab298780a64",
        # Note: rules_rust should point to the releases, not archive to avoid the hassle of bootstrapping in crate_universe.
        # This is described in https://bazelbuild.github.io/rules_rust/crate_universe.html#setup, otherwise bootstrap
        # is required which in turn requires a system CC toolchains, not the bazel controlled ones.
        urls = ["https://github.com/bazelbuild/rules_rust/releases/download/{version}/rules_rust-{version}.tar.gz"],
        use_category = [
            "controlplane",
            "dataplane_core",
            "dataplane_ext",
        ],
        extensions = ["envoy.wasm.runtime.wasmtime"],
...
```
Oh, cool somehow related to WASM and wasmtime! This aligns with my goal. Let's try running this referenced command `CARGO_BAZEL_REPIN=1 bazel sync --only=crate_index`. Nope, same error related to dynamically-linked executables.

```
Command
[/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel,
"splice",
"--output-dir",
/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/splicing-output,
"--splicing-manifest",
/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/splicing_manifest.json,
"--config",
/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel.json,
"--cargo",
/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/bin/cargo,
"--rustc",
/home/mccurdyc/.cache/bazel/_bazel_mccurdyc/3e696febca1fb3435f06295bae002db4/external/rust_linux_x86_64__x86_64-unknown-linux-gnu__stable_tools/bin/rustc,
"--cargo-lockfile",
/home/mccurdyc/src/github.com/mccurdyc/envoy/source/extensions/dynamic_modules/sdk/rust/Cargo.lock,
"--nonhermetic-root-bazel-workspace-dir",
/home/mccurdyc/src/github.com/mccurdyc/envoy]
failed
with
exit
code
127.
```

Okay, looks like it's using bazel-fetched dependencies instead of using system dependencies for `cargo` and `rustc`. How can we tell it to use the system dependencies?

Okay, let's go back to `bazel/dependency_imports.bzl`. The following look like they may be related 

```python
load("@rules_rust//rust:defs.bzl", "rust_common")                                                                                     
load("@rules_rust//rust:repositories.bzl", "rules_rust_dependencies", "rust_register_toolchains", "rust_repository_set")  
```

Why do I not see `defs.bzl` in the repo? Let's ask AI.
 
"This loads the `rust_common` provider from the `defs.bzl` file in the `@rules_rust` repository. `rust_common` is a Starlark provider that exposes Rust-specific build information"

https://github.com/bazelbuild/rules_rust and https://bazelbuild.github.io/rules_rust/. Let's look for `rust_register_toolchains` in the Envoy repo. Oh back in `bazel/dependency_imports.bzl` . What do these imported functions from `rules_rust` do? How can I tell `rules_rust` to use system dependencies instead of managing it's own dependencies? [A quick GitHub search](https://github.com/search?q=repo%3Abazelbuild%2Frules_rust%20%20rust_register_toolchains&type=code). And [these docs](https://bazelbuild.github.io/rules_rust/#bzlmod-1) look promising for maybe specifying "override" for using local rust. I remembered seeing Nix patches to override things related to rust in the official Nixpkgs envoy package.

I see [this block in Nixpkgs envoy](https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/package.nix#L89-L98) 

```python
# making a dir
mkdir -p bazel/nix/
# copying some local bazel BUILD file template and using system bash $(type -p bash) => bash is /run/current-system/sw/bin/bash)
substitute ${./bazel_nix.BUILD.bazel} bazel/nix/BUILD.bazel \
    --subst-var-by bash "$(type -p bash)"

# using Nix binaries
ln -sf "${cargo}/bin/cargo" bazel/nix/cargo
ln -sf "${rustc}/bin/rustc" bazel/nix/rustc
ln -sf "${rustc}/bin/rustdoc" bazel/nix/rustdoc
ln -sf "${rustPlatform.rustLibSrc}" bazel/nix/ruststd

substituteInPlace bazel/dependency_imports.bzl \
    --replace-fail 'crate_universe_dependencies()' 'crate_universe_dependencies(rust_toolchain_cargo_template="@@//bazel/nix:cargo", rust_toolchain_rustc_template="@@//bazel/nix:rustc")' \
    --replace-fail 'crates_repository(' 'crates_repository(rust_toolchain_cargo_template="@@//bazel/nix:cargo", rust_toolchain_rustc_template="@@//bazel/nix:rustc",'
```

Oh wow [there's a lot of good context in this BUILD file template](https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/bazel_nix.BUILD.bazel). I see an `export_files` function that if I had to guess means that these binaries are "returned" from this bazel file?

```python
exports_files(["cargo", "rustdoc", "ruststd", "rustc"])                                                                       
```

Then a list of toolchains. Presumably these are the Nix "systems" we are building for.

```python
toolchains = {                                                                                                                
	"x86_64": "x86_64-unknown-linux-gnu",                                                                                     
	"aarch64": "aarch64-unknown-linux-gnu",                                                                                   
}     
```

Nothing too interesting yet. Then, I see `rust_toolchain` which I know is related to "installing Rust" in Bazel via `rules_rust`. Why is it called "rules"`_rust` What does "rules" mean in Bazel? [Here are the docs](https://bazel.build/extending/rules) "A **rule** defines a series of [**actions**](https://bazel.build/extending/rules#actions) that Bazel performs on inputs to produce a set of outputs" ... "the [rule](https://bazel.build/rules/lib/globals/bzl#rule) function to define a new rule, and store the result in a global variable."

```python
[
    rust_toolchain(
        name = "rust_nix_" + k + "_impl",
        binary_ext = "",
        dylib_ext = ".so",
        exec_triple = v,
        cargo = ":cargo",
        rust_doc = ":rustdoc",
        rust_std = ":ruststd",
        rustc = ":rustc",
        stdlib_linkflags = ["-ldl", "-lpthread"],
        staticlib_ext = ".a",
        target_triple = v,
    )
    for k, v in toolchains.items()
]
```

And presumably, this adds some annonymous list of toolchain items to the Bazel build/workspace's global variable. And it looks like we are telling `rules_rust` a few things. Like prefix the name in each toolchain item "rust_nix". Okay let's go look at what `rust_toolchain` does with these input attribute values. Wait I don't see `rust_toolchain` in the `rules_rust` docs [here](https://bazelbuild.github.io/rules_rust/rust.html) . Does `rust_toolchain` come from `rules_rust`? Oh, [yes](https://bazelbuild.github.io/rules_rust/rust_toolchains.html?highlight=rust_toolchain#rust_toolchain) . Cool. For a second I thought my mental model was broken. 

Okay, back to the input attributes. `name`, cool. `binary_ext` "The extension for binaries created from rustc.". Okay, unset. We aren't producing binaries? I guess that makes sense. `dylib_ext` "The extension for dynamic libraries created from rustc." Okay, yeah probably the WASM stuff. Makes sense. `exec_triple` "The platform triple for the toolchains execution environment.". 

What is a "triple"? It links to these docs https://docs.bazel.build/versions/master/skylark/rules.html#configurations. Eh not that interesting; we'll come back if we need to. Seems to be related with the build environment. And we pass the toolchains value item to it. Oh, so "x86_64-unknown-linux-gnu" oh okay. 

Next. `cargo`, `":cargo"`. What is the `:` for? I've seen it in a few places in Bazel, so I'm assuming it's somehow referencing some `:cargo` attribute of some rule?? What are our imports again? Not helpful. Okay, just leaving this as a weak mental model note "refers to an attribute that may be overridden somewhere with 'nix-installed local rust'". Same for `:rustdoc` `:ruststd` and `rustc`. `stdlib_linkflags`. Oh wait, let's go back to the `rules_rust` docs for `cargo` "The location of the `cargo` binary. Can be a direct source or a filegroup containing one item". Ohh this is super relevant "filegroup" and "direct source" seem related to "rust install location", but ":cargo" weird. Come back to this. Oh `:` is a "label". Cool. Label "somewhere". 

"stdlib_linkflags" sounds like a very easy thing to Google "rust stdlib linkflags" https://doc.rust-lang.org/reference/linkage.html . Eh, let's have AI parse the docs and tell me what these specific flags do. "- **`-lpthread`**: Required because Rust's stdlib uses threads and synchronization primitives that rely on POSIX threads.". Sure "required" and something related to rust using threads, sounds legit. "- **`-ldl`**: Needed for dynamic loading features (e.g., `std::os::unix::ffi::OsStrExt` and dynamic library loading APIs) that require the dynamic loader library." "dynamically loading features" "APIs" that require the "loader library". Hm maybe related to "WASM" "feature". Sounds legit. Now, if you asked me what other flags, :shrug:. Let's just keep the rust "linkage" docs tab open.

Go through my tabs, what can I close now? Where was the root of this thought again? Something related to the bazel build template file in nixpkgs/envoy. `staticlib_ext` ".a" sure seems legit. Okay `rust_toolchain`. We pass a bunch of input attributes that don't seem all that impactful other than the Nix system. Well and those "labels". Those seem super important. Let's look up "bazel labels" - https://bazel.build/concepts/labels. 

Oh I saw a ton of these types of things `@@myrepo//my/app/main:app_binary` in nixpkgs/envoy. "The first part of the label is the repository name, `@@myrepo`". Okay, repository sounds like "source location" "The double-`@` syntax signifies that this is a [_canonical_ repo name](https://bazel.build/external/overview#canonical-repo-name), which is unique within the workspace" - https://bazel.build/external/overview#canonical-repo-name "The name by which a repository is always addressable. Within the context of a workspace, each repository has a single canonical name. A target inside a repo whose canonical name is `canonical_name` can be addressed by the label `@@canonical_name//package:target` (note the double `@`).". Oh and also super important "The main repository always has the empty string as the canonical name.". Oh so like, ":target". Cool.

Tab check:
- [root thought nixpkgs/envoy](https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/package.nix#L89-L98)
- [rust_toolchain in rules_rust](https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/bazel_nix.BUILD.bazel#L12)
- [rust_toolchain docs](https://bazelbuild.github.io/rules_rust/rust_toolchains.html?highlight=rust_toolchain#rules) Although at this point, I think these can be closed. At this point, we can assume this installs the rust toolchain based on labels. We need to understand the values of these labels now.

Okay, `:cargo` `:rustc` labels in `nixpkgs/envoy`. Some other `toolchain` that isn't rust, but still somehow related to "nix_rust". Then, `local_sh_impl`. "impl" is like Bazel function. And then, `@bash@` so the "repository name". Hm seems kinda special with the trailing `@`. It's just bash, we'll come back to this. I want to see something that references a local filepath. Okay nothing else in this BUILD template related to local filepaths. Let's close this tab and go back to the root of nixpkgs/envoy. 

Applying patches, postPatch doing some substitution that I would expect to reference nixpkg paths. And I see lots of symlink creation that looks very relevant.

```python
# using Nix binaries
ln -sf "${cargo}/bin/cargo" bazel/nix/cargo
ln -sf "${rustc}/bin/rustc" bazel/nix/rustc
ln -sf "${rustc}/bin/rustdoc" bazel/nix/rustdoc
ln -sf "${rustPlatform.rustLibSrc}" bazel/nix/ruststd
```

Oh okay, so apply normal Git patches for Python, Go, CC toolchain and using a newer `rules_rust` bazel version. Maybe for these we are actually making larger changes and want to install these in a completely different way than the Envoy repo,  but then for patching Rust, we are using exactly what's in the Envoy repo, but overriding the output binaries with nix binary paths. Let's look at the CC toolchain as this is probably the most important first. It relates to those critical system build tooling and we'll definitely want to tweak these for Nix package paths and Envoy is C++, so probably heavily relies on these libraries. Rust is probably more for the WASM extension.

```diff
# https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/0003-nixpkgs-use-system-C-C-toolchains.patch#L20-L25

-    rules_foreign_cc_dependencies()
+    rules_foreign_cc_dependencies(
+       register_default_tools=False,  # no prebuilt toolchains
+	    register_built_tools=False,  # nor from source
+	    register_preinstalled_tools=True,  # use host tools (default)
+    )
```

Oh okay, before using default values. What's `rules_foreign_cc_dependencies()` let's go Google for this Bazel rules package. Also, we see this is a patch for the `bazel/dependency_imports.bzl` file. Let's go look at this file in the Envoy repo [here](https://github.com/mccurdyc/envoy/blob/c01676e090c94fe4ee720534146a4f177931530d/bazel/dependency_imports.bzl#L35            ) . Oh cool it's under `envoy_dependency_imports()`. Seems extremely relevant. Oh yeah, this is that place with `crates_repository()`. Where were we again? Oh something with `cc` dependencies and `rules_foreign_cc_dependencies()`

```python
load("@rules_foreign_cc//foreign_cc:repositories.bzl", "rules_foreign_cc_dependencies") 
```

Okay, I think I can describe this now. Loads a rule "rules_foreign_cc_dependencies" from a "@rules_foreign_cc" repo. Something `//` maybe path related? And `repositories.bzl` file in that repo. Let's just go look up this package. Oh [here](https://github.com/mccurdyc/envoy/blob/c01676e090c94fe4ee720534146a4f177931530d/mobile/WORKSPACE#L18). Tries to download from GCS, then falls back to http://github.com/engflow/rules_foreign_cc "Rules for building C/C++ projects using foreign build systems inside Bazel projects." Links to this page that 404s - https://bazelbuild.github.io/rules_foreign_cc. Okay back to the root thought. We were just trying to see what a few input args did

```diff
+       register_default_tools=False,  # no prebuilt toolchains
+	    register_built_tools=False,  # nor from source
+	    register_preinstalled_tools=True,  # use host tools (default)
```

I mean the comments in nixpkgs/envoy are super helpful, but I want to read these in official docs, not just assume this is correct. I just want to learn about these params, not sift through some massive repo's code - https://github.com/bazel-contrib/rules_foreign_cc. I'm just going to search the repo for these https://github.com/search?q=register_default_tools%20repo%3Abazel-contrib%2Frules_foreign_cc%20&type=code Oh, there are apparently input docs under the `docs/` dir. Let's go. Yes, this is what I wanted - https://github.com/bazel-contrib/rules_foreign_cc/tree/main/docs. Cool, this is what we want - https://github.com/bazel-contrib/rules_foreign_cc/tree/main/docs#rules_foreign_cc_dependencies

`register_default_tools` - "If True, the cmake and ninja toolchains, calling corresponding preinstalled binaries by name (cmake, ninja) will be registered after 'native_tools_toolchains' without any platform constraints. The default is True." Ooh "default true". Yeah, nope. Ah same for the other inputs. Cool. Telling it to NOT use local cc toolchain things, but instead presumably, we will ... oh wait "preinstalled_tools=True". We DO want this to use system tools installed via nix. So the Falses above are saying "I don't want these tools at all"? Okay something related about telling bazel to either use host tools or not for cc toolchain. Let's go back to nixpkgs/envoy root. `0003-nixpkgs-use-system-C-C-toolchains.patch` makes sense.

Oh there's a `rules_rust` patch. Is this just the version specification? https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/rules_rust.patch No. Looks like telling `rules_rust` to use specific paths instead of watching dirs for cargo bootstrapping and cargo crates? Wait, this is rust. We don't care about rust yet. Still C++ compilation. nixpkgs/envoy `package.nix` Why did we need the BUILD template again?
### nixpkgs/envoy package.nix `postPatch`

```python
 substituteInPlace bazel/dependency_imports.bzl \
      --replace-fail 'crate_universe_dependencies()' 'crate_universe_dependencies(rust_toolchain_cargo_template="@@//bazel/nix:cargo", rust_toolchain_rustc_template="@@//bazel/nix:rustc")' \
      --replace-fail 'crates_repository(' 'crates_repository(rust_toolchain_cargo_template="@@//bazel/nix:cargo", rust_toolchain_rustc_template="@@//bazel/nix:rustc",
```

We are essentially applying a patch, but just a simple string substitution in `bazel/dependency_imports.bzl`. We are ... wait this is rust stuff, skip? Eh. No, let's spend a second on the mental model. `crate_universe_dependencies`, updating `rust_toolchain_cargo_template` to use `@@//bazel/nix:cargo`. Oh what!? `:cargo` that looks like a label! `/bazel/nix` is the path used in nixpkgs/envoy's `mkdir -p`. `@@` ? Wait, wasn't that like the "default" repo or local repo or something. Oh, the local workspace is our BUILD template file. Wait, but we are in the Envoy repo in the Nix build VM, right? Where is `/bazel/nix` in the Envoy repo structure? I should try to do an `ls` in the nix build. Not worth. I know that's what it is. Oh okay. so this block updates the `bazel/dependency_imports.bzl` file in the Envoy repo to tell it to pull crates --- or all of rust things from the definition of `:cargo` and `:rustc` that will be in a `/bazel/nix/BUILD.bazel` file that will be in the Nix VM during `postPatch`

```python
 # patch rules_rust for envoy specifics, but also to support old Bazel
# (Bazel 6 doesn't have ctx.watch, but ctx.path is sufficient for our use)
cp ${./rules_rust.patch} bazel/rules_rust.patch
substituteInPlace bazel/repositories.bzl \
    --replace-fail ', "@envoy//bazel:rules_rust_ppc64le.patch"' ""
```

Oh overwrites the `bazel/rules_rust.patch` in the Envoy repo with the local `rules_rust.patch` file and then overwrites or removes "@envoy//bazel:rules_rust_ppc64le.patch" from `bazel/repositories.bzl`. 

Okay I don't really care about these things yet. Still just trying to get Envoy building locally not in Nix yet. But NixOS doesn't like dyanmically-loaded executables. What were the executables it was trying to use again? Oh it was rust related `cargo` and `rustc`. So we need to fix these two paths. And we looked at nixpkgs/envoy just to get an idea of how it could be done and it was doing a bunch of bazel-native overwriting binary path things.

Using `pkgs.applyPatches` and now `"error: undefined variable 'cargo'"` `"ln -sf "${cargo}/bin/cargo" bazel/nix/cargo"` oh okay make sure this points to the path of Nix cargo. Oh adding `pkgs` in front of everything makes sense because when you are IN nixpkgs, you have access to these, but I'm in a `flake.nix` in the Envoy repo.

`direnv reload` succeeded. Okay. Time for another `nix build`? Or were we just running `bazel build` directly? Let's try `nix build` for fun. Wait, actually I think we will HAVE to use `nix build` since it will apply all the patches, etc. 

```bash
       >                fail(_EXECUTE_ERROR_MESSAGE.format(
       > Error in fail: Command [/tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modules_rust_sdk_crate_index
/cargo-bazel, "splice", "--output-dir", /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modules_rust_sdk_crat
e_index/splicing-output, "--splicing-manifest", /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modules_rust_
sdk_crate_index/splicing_manifest.json, "--config", /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modules_r
ust_sdk_crate_index/cargo-bazel.json, "--cargo", /tmp/nix-build-envoy-deps.tar.gz.drv-0/hx85kmm7pi75hyx46cjgissmkks61jgb-sou
rce-patched/bazel/nix/cargo, "--rustc", /tmp/nix-build-envoy-deps.tar.gz.drv-0/hx85kmm7pi75hyx46cjgissmkks61jgb-source-patch
ed/bazel/nix/rustc, "--cargo-lockfile", /tmp/nix-build-envoy-deps.tar.gz.drv-0/hx85kmm7pi75hyx46cjgissmkks61jgb-source-patch
ed/source/extensions/dynamic_modules/sdk/rust/Cargo.lock, "--nonhermetic-root-bazel-workspace-dir", /tmp/nix-build-envoy-dep
s.tar.gz.drv-0/hx85kmm7pi75hyx46cjgissmkks61jgb-source-patched] failed with exit code 127.
       > STDOUT ------------------------------------------------------------------------
       >
       > STDERR ------------------------------------------------------------------------
       > Could not start dynamically linked executable: /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modul
es_rust_sdk_crate_index/cargo-bazel
       > NixOS cannot run dynamically linked executables intended for generic
       > linux environments out of the box. For more information, see:
       > https://nix.dev/permalink/stub-ld
```

Okay, I see lots of `.drv`s that's a good sign! And `/tmp` paths to things. This looks like it's definitely replacing path. But Nix is still unhappy about trying to use `/tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/dynamic_modules_rust_sdk_crate_index/cargo-bazel`. Okay, I didn't apply any patches for `cargo-bazel`. And I remember that `cargo-bazel` was replaced or proceeded by `rules_rust` and I remember seeing something related to `rules_rust` in the nixpkgs/envoy. Oh I think the important thing is that it sets the rustc and cargo versions to "hermetic" instead of a legit version. Maybe that legit version was referencing some old path that doesn't have `cargo-bazel`.

1a0f2d8b8d

```bash
nix build

error: path '/nix/store/75aiyjh0b4limr4j6ampxsm92zk08p89-source/nix/patches/rules_rust_extra.patch' does not exist
``` 

Oh, I must have screwed up paths. Am I being fancy trying to store these nix files under `nix/` in the Envoy repo?

ea6adc06dd

```bash
nix build
...
       > ERROR: /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/bazel_tools/tools/build_defs/repo/utils.bzl:202:22: A
n error occurred during the fetch of repository 'rules_rust':
...
Error in patch: Error applying patch /tmp/nix-build-envoy-deps.tar.gz.drv-0/kr3xyim0f52wmwhpqpc7fy9b546z1cgh-source-patched/bazel/rules_rust.patch: in patch applied to /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/rules_rust/cargo/private/cargo_bootstrap.bzl: could not apply patch due to CONTENT_DOES_NOT_MATCH_TARGET, error applying change near line 173
```

Okay, so it successfully failed to apply my patch ;P. Something related to `cargo_bootstrap.bzl` and "CONTENT_DOES_NOT_MATCH_TARGET" near some line 173. Maybe something related to a cargo bootstrap / rust toolchain hash that doesn't match? I remember seeing things related to this in the nixpkgs/envoy code. Okay, it's under `fetchAttrs`. Okay related to fetching which is probably before "patching", right. You must fetch the code into the Nix VM before you can apply patches. 

Why is this substitution in `fetchAttrs` instead of during the patch phase like the others? Oh because `fetchAttrs` is specific to a fetching phase of BAZEL; NOT nix fetching. So this needs to be applied before a `bazel build` command runs. So theoretically, it could be applied in the Nix fetching / patching phase. Let's put it in there to keep it altogether.

```python
substituteInPlace bazel/dependency_imports.bzl \
    --replace-fail 'crate_universe_dependencies(' 'crate_universe_dependencies(bootstrap=True, ' \
    --replace-fail 'crates_repository(' 'crates_repository(generator="@@cargo_bazel_bootstrap//:cargo-bazel", '
'';
```

Oh maybe because this is the same `bazel/dependency_imports.bzl` file modified above and we don't want these changes to be applied until BAZEL is in it's fetch phase (not sure if Bazel runs other things first.). Let's put in the `fetchAttrs` `postPatch` phase like nixpkgs/envoy.

Oh and here's the thing called `cargo-bazel`

```python
# Install repinned rules_rust lockfile
cp source/extensions/dynamic_modules/sdk/rust/Cargo.Bazel.lock $bazelOut/external/Cargo.Bazel.lock

# Don't save cargo_bazel_bootstrap or the crate index cache
rm -rf $bazelOut/external/cargo_bazel_bootstrap $bazelOut/external/dynamic_modules_rust_sdk_crate_index/.cargo_home $bazelOut/external/dynamic_modules_rust_sdk_crate_index/
```

Okay if we are failing to have matching hashes, maybe we just copy or remove things, right? Seems like that's what these do.


Bazel in a Nix VM for building Envoy is failing to fetch `rules_rust` because of "no such package '@@rules_rust//crate_universe/private'". Okay, is it failing to run a hash function to calculate the new hash to overwrite the old? I see something that looks like it may tweak cargo tree things

```python
     # Remove references to paths in the Nix store.
      sed -i \
        -e 's,${python3},__NIXPYTHON__,' \
        -e 's,${stdenv.shellPackage},__NIXSHELL__,' \
        -e 's,${builtins.storeDir}/[^/]\+/bin/bash,__NIXBASH__,' \
        $bazelOut/external/com_github_luajit_luajit/build.py \
        $bazelOut/external/local_config_sh/BUILD \
        $bazelOut/external/*_pip3/BUILD.bazel \
        $bazelOut/external/rules_rust/util/process_wrapper/private/process_wrapper.sh \
        $bazelOut/external/rules_rust/crate_universe/src/metadata/cargo_tree_rustc_wrappe
```

`$bazelOut` must be some path set by Nix's `buildBazelPackage`. Okay back to the `buildBazelPackage` definition - https://github.com/NixOS/nixpkgs/blob/master/pkgs/build-support/build-bazel-package/default.nix. Now that we understand things a bit more, we'll definitely want to come back to this definition. Okay `$bazelOut/external` must be something created during the fetch phase of Bazel.

```bash
export bazelOut="$(echo ''${NIX_BUILD_TOP}/output | sed -e 's,//,/,g')"
```

Okay, I remember seeing nixpkgs/envoy set all of these `remove...` attributes to true. These clean up a bunch of files

```python
# Remove all built in external workspaces, Bazel will recreate them when building
rm -rf $bazelOut/external/{bazel_tools,\@bazel_tools.marker}
${lib.optionalString removeRulesCC "rm -rf $bazelOut/external/{rules_cc,\\@rules_cc.marker}"}

rm -rf $bazelOut/external/{embedded_jdk,\@embedded_jdk.marker}
${lib.optionalString removeLocalConfigCc "rm -rf $bazelOut/external/{local_config_cc,\\@local_config_cc.marker}"}
${lib.optionalString removeLocal "rm -rf $bazelOut/external/{local_*,\\@local_*.marker}"}

# For bazel version >= 6 with bzlmod.
${lib.optionalString removeLocalConfigCc "rm -rf $bazelOut/external/*[~+]{local_config_cc,local_config_cc.marker}"}
${lib.optionalString removeLocalConfigSh "rm -rf $bazelOut/external/*[~+]{local_config_sh,local_config_sh.marker}"}
${lib.optionalString removeLocal "rm -rf $bazelOut/external/*[~+]{local_jdk,local_jdk.marke
```

Let's set them all! Why not!?

```nix
# Newer versions of Bazel are moving away from built-in rules_cc and instead
# allow fetching it as an external dependency in a WORKSPACE file[1]. If
# removed in the fixed-output fetch phase, building will fail to download it.
# This can be seen e.g. in #73097
#
# This option allows configuring the removal of rules_cc in cases where a
# project depends on it via an external dependency.
#
# [1]: https://github.com/bazelbuild/rules_cc
removeRulesCC ? true,
removeLocalConfigCc ? true,
removeLocalConfigSh ? true,
removeLocal ? true,

# Use build --nobuild instead of fetch. This allows fetching the dependencies
# required for the build as configured, rather than fetching all the dependencies
# which may not work in some situations (e.g. Java code which ends up relying on
# Debian-specific /usr/share/java paths, but doesn't in the configured build).
fetchConfigured ? true,

# Don’t add Bazel --copt and --linkopt from NIX_CFLAGS_COMPILE /
# NIX_LDFLAGS. This is necessary when using a custom toolchain which
# Bazel wants all headers / libraries to come from, like when using
# CROSSTOOL. Weirdly, we can still get the flags through the wrapped
# compiler.
dontAddBazelOpts ? false
```

Oh they default to true.

Oh from nixpkgs/envoy, I was thinking of


```nix
fetchAttrs = {
...
    dontUseCmakeConfigure = true;
    dontUseGnConfigure = true;
}

buildAttrs = {
    dontUseCmakeConfigure = true;
    dontUseGnConfigure = true;
    dontUseNinjaInstall = true;
    ...
}
```

Let's read ths nix docs on these:
- https://nixos.org/manual/nixpkgs/stable/#dont-use-cmake-configure - "When set to true, don’t use the predefined `cmakeConfigurePhase`." Okay. I can't find the others, but sounds like not running some Nix configure phase for a few tools. Sure.

Am I missing build tools? Nah that wasn't it. Let's see if we can get in to the Nix sandbox during the build and see what are in these files

```bash
bazel/rules_rust.patch: in patch applied to /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/rules_rust/cargo/private/cargo_bootstrap.bzl: could not apply patch due to CONTENT_DOES_NOT_MATCH_TARGET, error applying change near line 173
```

```nix
fetchAttrs = {
...
	nativeBuildInputs = [
	  ...
	  breakpointHooks
	]
}
```

```
nix build
(buildPhase): sudo /nix/store/y528s2cvrah7sgig54i97gnbq3nppikp-attach/bin/attach 9248072
```
In another shell `sudo /nix/store/y528s2cvrah7sgig54i97gnbq3nppikp-attach/bin/attach 9248072`

```bash
[root@nuc:~/q9m992myg24ysld1rbg9iyq3si6bqdx5-source-patched]# echo $bazelOut
/tmp/nix-build-envoy-deps.tar.gz.drv-0/output
```

AHH! Now we are making new progres!! Let's Go!

```
[root@nuc:~/output]# ls -al $bazelOut/external
total 80
drwxr-xr-x 10 nixbld1 nixbld 4096 Jun 15 21:03 .
drwxr-xr-x  4 nixbld1 nixbld 4096 Jun 15 21:03 ..
drwxr-xr-x 11 nixbld1 nixbld 4096 Jun 15 21:03 aspect_bazel_lib
-rw-r--r--  1 nixbld1 nixbld  211 Jun 15 21:03 @aspect_bazel_lib.marker
drwxr-xr-x  6 nixbld1 nixbld 4096 Jun 15 21:03 bazel_features
-rw-r--r--  1 nixbld1 nixbld  118 Jun 15 21:03 @bazel_features.marker
drwxr-xr-x  5 nixbld1 nixbld 4096 Jun 15 21:03 bazel_skylib
-rw-r--r--  1 nixbld1 nixbld  118 Jun 15 21:03 @bazel_skylib.marker
lrwxrwxrwx  1 nixbld1 nixbld   98 Jun 15 21:03 bazel_tools -> /tmp/nix-build-envoy-deps.tar.gz.drv-0/tmp/install/6251dd5fd6d67ca8664b3aad027639bb/embedded_tools
-rw-r--r--  1 nixbld1 nixbld   65 Jun 15 21:03 @bazel_tools.marker
drwxr-xr-x  8 nixbld1 nixbld 4096 Jun 15 21:03 com_google_googleapis
-rw-r--r--  1 nixbld1 nixbld  118 Jun 15 21:03 @com_google_googleapis.marker
drwxr-xr-x  6 nixbld1 nixbld 4096 Jun 15 21:03 emsdk
-rw-r--r--  1 nixbld1 nixbld  210 Jun 15 21:03 @emsdk.marker
drwxr-xr-x  2 nixbld1 nixbld 4096 Jun 15 21:03 envoy_api
-rw-r--r--  1 nixbld1 nixbld  145 Jun 15 21:03 @envoy_api.marker
drwxr-xr-x  8 nixbld1 nixbld 4096 Jun 15 21:03 proxy_wasm_cpp_host
-rw-r--r--  1 nixbld1 nixbld  224 Jun 15 21:03 @proxy_wasm_cpp_host.marker
drwxr-xr-x 15 nixbld1 nixbld 4096 Jun 15 21:03 rules_python
-rw-r--r--  1 nixbld1 nixbld  118 Jun 15 21:03 @rules_python.marker
```

Now this path makes sense `/tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/rules_rust/cargo/private/cargo_bootstrap.bzl`

Oh, interesting, there is NO `$bazelOut/external/rules_rust`. So our Nix stuff failed to configure Bazel correctly to apply our patches. Maybe I need to `breakpointHook` earlier in the Nix build?

Ohh actually, let's try running bazel commands directly in here

```bash
[root@nuc:~/q9m992myg24ysld1rbg9iyq3si6bqdx5-source-patched]# bazel version
Build label: 7.6.0- (@non-git)
Build target: @@//src/main/java/com/google/devtools/build/lib/bazel:BazelServer
Build time: Tue Jan 1 00:00:00 1980 (315532800)
Build timestamp: 315532800
Build timestamp as int: 315532800
```

Are my patches here in this "source-patched"? Let's look at `bazel/dependency_imports.bzl`

```bash
[root@nuc:~/q9m992myg24ysld1rbg9iyq3si6bqdx5-source-patched]# cat bazel/dependency_imports.bzl | tail -n 10
        version = go_version,
    )

def crates_repositories():
    crates_repository(generator="@@cargo_bazel_bootstrap//:cargo-bazel", rust_toolchain_cargo_template="@@//bazel/nix:cargo", rust_toolchain_rustc_template="@@//bazel/nix:rustc",
        name = "dynamic_modules_rust_sdk_crate_index",
        cargo_lockfile = "@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.lock",
        lockfile = Label("@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.Bazel.lock"),
        manifests = ["@envoy//source/extensions/dynamic_modules/sdk/rust:Cargo.toml"],
    )
```

Where did my Nix flake say to install `rules_rust`? Oh, `bazel/`. But I do see other things in `bazel/nix` too which is good!

```bash
[root@nuc:~/q9m992myg24ysld1rbg9iyq3si6bqdx5-source-patched]# ls bazel/nix/
BUILD.bazel  cargo  rules_rust_extra.patch  rustc  rustdoc  ruststd
```

```bash
32 diff --git cargo/private/cargo_bootstrap.bzl cargo/private/cargo_bootstrap.bzl
33 index a8021c49d62037ef32c7c64d5bb4a5efe3a8b4aa..f63d7c23ae0bddc9f3fece347a3a2b5b0afe6d8d 100644
34 --- cargo/private/cargo_bootstrap.bzl
35 +++ cargo/private/cargo_bootstrap.bzl
36 @@ -173,13 +173,13 @@ def _detect_changes(repository_ctx):
37      # 'consumed' which means changes to it will trigger rebuilds
38  
39      for src in repository_ctx.attr.srcs:
40 -        repository_ctx.watch(src)
41 +        repository_ctx.path(src)
42  
43 -    repository_ctx.watch(repository_ctx.attr.cargo_lockfile)
44 -    repository_ctx.watch(repository_ctx.attr.cargo_toml)
45 +    repository_ctx.path(repository_ctx.attr.cargo_lockfile)
...
```

Okay this is where the line 173 is coming from, so something in cargo_bootstrap.bzl. Okay and actually this error is related to failing to apply the patch --- kinda like a merge conflict. This is what is actually in rules_rust https://github.com/bazelbuild/rules_rust/blob/0cb272d303ce7ea1dbe9bb5b16228f2008c8d72e/cargo/private/cargo_bootstrap.bzl#L173. Oh okay, maybe this is a rules_rust version mismatch. I remember seeing this - https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/0004-nixpkgs-bump-rules_rust-to-0.60.0.patch I manually made this change in the Envoy source repo and re-run `nix build` and got a new error!

```bash
Error in patch: Error applying patch /tmp/nix-build-envoy-deps.tar.gz.drv-0/cnl8sygl2j3p6127cgfkxjx3qss66rc2-source-patched/bazel/rules_rust_ppc64le.patch: in patch applied to /tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/rules_rust/MODULE.bazel: could not apply patch due to CONTENT_DOES_NOT_MATCH_TARGET, error applying change near line 19
       > ERROR: Error computing the main repository mapping: no such package '@@rules_rust//crate_universe/private': Error applying patch /tmp/nix-build-envoy-deps.tar.gz.drv-0/cnl8sygl2j3p6127cgfkxjx3qss66rc2-source-patched/bazel/rules_rust_ppc64le.patch
```

I remember seeing nixpkgs/envoy get rid of `rules_rust_ppc64le` [here](https://github.com/mccurdyc/nixpkgs/blob/80fbf5d705a48e091b860235a64dec9c7eabf070/pkgs/by-name/en/envoy/package.nix#L100-L104)

Oh wow it's installing rust crates now!! It's making it further!! Okay that's enough for today.

```bash
/tmp/nix-build-envoy-deps.tar.gz.drv-0/output/external/python3_12_host/python
> NixOS cannot run dynamically linked executables intended for generic
```

Okay, I know how to solve these now. Let's get into the Nix sandbox and check which python.

I'm going to need to do a patch or a post-Bazel-install in-place substitution of Bazel's
Python so that it uses the sandbox Python instead. But first, let's see where Bazel tries
to use Python 3.12. It's probably in `bazel/dependency_imports.bzl`. Hmm doesn't
seem like it. I see some `pip3` things. Let's look at the error again to see if that
gives a hint.

```bash
nix build
...
> no configure script, doing nothing
> Running phase: buildPhase
> ERROR: The project you're trying to build requires Bazel 7.6.0 (specified in /build/s8pzcp058ywsnmzdp0xs4sgigyqglgm1-source-patched/.bazelversion), but it wasn't found in /nix/store/8nbnr7vc86cp6nw92s9v7k3ab9028vr2-bazel-6.5.0/bin.
>
> Bazel binaries for all official releases can be downloaded from here:
>   https://github.com/bazelbuild/bazel/releases
>
> Please put the downloaded Bazel binary into this location:
>   /nix/store/8nbnr7vc86cp6nw92s9v7k3ab9028vr2-bazel-6.5.0/bin/bazel-7.6.0-linux-x86_64
```

```bash
sudo /nix/store/y528s2cvrah7sgig54i97gnbq3nppikp-attach/bin/attach 3412430
bash-5.2# cat .bazelversion
7.6.0
```

Oh it's still there even though I tried removing it.

```bash
bash-5.2# bazel build -c opt envoy
Extracting Bazel installation...
Starting local Bazel server and connecting to it...
INFO: Repository com_google_googleapis instantiated at:
  /build/r6mjfd99m7j2nn6qwg1ibnys453i0s1l-source-patched/WORKSPACE:9:23: in <toplevel>
  /build/r6mjfd99m7j2nn6qwg1ibnys453i0s1l-source-patched/bazel/api_repositories.bzl:4:21: in envoy_api_dependencies
  /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/envoy_api/bazel/repositories.bzl:27:26: in api_dependencies
  /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/envoy_api/bazel/repositories.bzl:9:23: in external_http_archive
  /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/envoy_api/bazel/envoy_http_archive.bzl:16:17: in envoy_http_archive
Repository rule http_archive defined at:
  /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/bazel_tools/tools/build_defs/repo/http.bzl:372:31: in <toplevel>
WARNING: Download from https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz failed: class com.google.devtools.build.lib.bazel.repository.downloader.UnrecoverableHttpException Unknown host: github.com
ERROR: An error occurred during the fetch of repository 'com_google_googleapis':
   Traceback (most recent call last):
        File "/build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/bazel_tools/tools/build_defs/repo/http.bzl", line 132, column 45, in _http_archive_impl
                download_info = ctx.download_and_extract(
Error in download_and_extract: java.io.IOException: Error downloading [https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz] to /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/com_google_googleapis/temp13342235895244228205/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz: Unknown host: github.com
ERROR: /build/r6mjfd99m7j2nn6qwg1ibnys453i0s1l-source-patched/WORKSPACE:9:23: fetching http_archive rule //external:com_google_googleapis: Traceback (most recent call last):
        File "/build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/bazel_tools/tools/build_defs/repo/http.bzl", line 132, column 45, in _http_archive_impl
                download_info = ctx.download_and_extract(
Error in download_and_extract: java.io.IOException: Error downloading [https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz] to /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/com_google_googleapis/temp13342235895244228205/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz: Unknown host: github.com
ERROR: Error computing the main repository mapping: no such package '@com_google_googleapis//': java.io.IOException: Error downloading [https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz] to /build/.cache/bazel/_bazel_root/f97a5d5d084e9180b40253ffbf680525/external/com_google_googleapis/temp13342235895244228205/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz: Unknown host: github.com
```

Looks like a few more things that I need to tell Bazel NOT to try to fetch.

Huh. I understand the failure. The nix sandbox can't fetch a `com_google_googleapis` repository from `github.com` which is instantiated in `./bazel/api_repositories.bzl`, specifically an `envoy_api_dependencies` function.
But I don't know what it is trying to get from there. I guess I can grep for references of `com_google_googleapis`.

I see in `api/bazel/repositories.bzl`. Maybe just remove this? But then references would fail. So `external_http_archive` seems like
it will try to fetch a repository from some external HTTP archive, which we know won't be possible in the nix sandbox, so let's try replacing
something that makes sense in `external_http_archive` which comes from the following function which says to fetch from some list of `REPOSITORY_LOCATIONS_SPEC`
defined in `repository_locations.bzl`. What if we just make this list of repos empty or somehow tell it to use a local directory?

```python
...
load(":repository_locations.bzl", "REPOSITORY_LOCATIONS_SPEC")

REPOSITORY_LOCATIONS = load_repository_locations(REPOSITORY_LOCATIONS_SPEC)

# Use this macro to reference any HTTP archive from bazel/repository_locations.bzl.
def external_http_archive(name, **kwargs):
    envoy_http_archive(
        name,
        locations = REPOSITORY_LOCATIONS,
        **kwargs
    )

def api_dependencies():
    ...
    external_http_archive(
        name = "com_google_googleapis",
    )
    ...
```

Okay in `api/bazel/repository_locations.bzl` I see

```
...
    com_google_googleapis = dict(
        # TODO(dio): Consider writing a Starlark macro for importing Google API proto.
        project_name = "Google APIs",
        project_desc = "Public interface definitions of Google APIs",
        project_url = "https://github.com/googleapis/googleapis",
        version = "fd52b5754b2b268bc3a22a10f29844f206abb327",
        sha256 = "97fc354dddfd3ea03e7bf2ad74129291ed6fad7ff39d3bd8daec738a3672eb8a",
        release_date = "2024-09-16",
        strip_prefix = "googleapis-{version}",
        urls = ["https://github.com/googleapis/googleapis/archive/{version}.tar.gz"],
        use_category = ["api"],
        license = "Apache-2.0",
        license_url = "https://github.com/googleapis/googleapis/blob/{version}/LICENSE",
    ),
...
```

But what would I even point this at locally? I don't think I can use `google-cloud-sdk`.

Oh this looks interesting

```python
bazel/repositories.bzl                                                                                                                      
1:load("@com_google_googleapis//:repository_rules.bzl", "switched_rules_by_language")                                                       
243:        name = "com_google_googleapis_imports", 
```

Oh and in `bazel/repositories.bzl` I see the following.

```python
...
    switched_rules_by_language(
        name = "com_google_googleapis_imports",
        cc = True,
        go = True,
        python = True,
        grpc = True,
    )
...
```

I got stuck for a while, then ended up querying AI for my error to give some suggestions
and came across the `--nofetch` Bazel flag.

Then, I encounter the following; which makes sense. These are the errors that I expected
to see. Now, I just need to figure out how to tell `@@bazel_tools` to reference
a local `bazel_tools`

```bash
> Computing main repo mapping:
> ERROR: Error computing the main repository mapping: no such package '@@bazel_tools//tools/build_defs/repo': to fix, run
>      bazel fetch //...
> External repository @@bazel_tools not found and fetching repositories is disabled.
```

Hmm `--nofetch` seems promising, but disabling temporarily

```
Error in download_and_extract: java.io.IOException: Error downloading [https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz] to /build/output/external/com_google_googleapis/temp4237767006948401698/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz: Unknown host: github.com
```

Okay, so it seems that it's trying to install `https://github.com/googleapis/googleapis/archive/fd52b5754b2b268bc3a22a10f29844f206abb327.tar.gz` to `$bazelOut/external/com_google_googleapis/...`
but it failing to reach github.com, which is expected. And I can't just tell
Nix to install to this directory I don't think.

What even is this? https://github.com/googleapis/googleapis ah cool yeah, I remember
asking if there were a nixpkg for this! I don't need a nixpkg, just `fetchTarball` or whatever.

Okay, I was starting to get quite frustrated. I couldn't understand how the nixpkgs/envoy
was doing this. Then I decided to dig more into why nixpkgs/envoy was explicitly
using `bazel_6` instead of `bazel_7` like the upstream envoy repo was explicitly calling for.

Turns out, from AI:

"The Envoy package in Nixpkgs uses `bazel_6` instead of `bazel_7` primarily for
compatibility and stability reasons. Bazel 7 introduced significant changes, most
notably the deprecation of the traditional `WORKSPACE` setup in favor of `bzlmod`,
Bazel's new module system. Many existing Bazel projects, including Envoy, have not
fully migrated to `bzlmod` and may rely on behaviors or APIs that were changed or removed in Bazel 7

```bash
find . -name "WORKSPACE"
./ci/osx-build-config/WORKSPACE
./mobile/third_party/rbe_configs/cc/WORKSPACE
./mobile/envoy_build_config/WORKSPACE
./mobile/WORKSPACE
./bazel/rbe/toolchains/configs/linux/gcc/cc/WORKSPACE
./bazel/rbe/toolchains/configs/linux/clang/cc/WORKSPACE
./WORKSPACE
```

```bash
find . -name "MODULE.bazel"
# (empty)
```

Ah okay. Envoy definitely doesn't use the new bzlmod module system yet.

## Back to Bazel 6

```bash
> ERROR: Error computing the main repository mapping: at /tmp/nix-build-envoy-deps.tar.gz.drv-0/2p08rkm66jm7makw26ipl3x4z279g9fp-source-patched/bazel/dependency_imports.bzl:2:6: Encountered error while reading extension file 'requirements.bzl': no such package '@base_pip3//': no such package '@python3_12_host//':
```
