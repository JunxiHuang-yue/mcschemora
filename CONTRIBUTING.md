# Contributing to MCSchemora

Install [uv](https://docs.astral.sh/uv/) and [Rust](https://rustup.rs/), then run
from the repository root:

```sh
make setup
```

The checkout selects Rust 1.88.0 through `rust-toolchain.toml` and Python 3.12
through `.python-version`. Python changes take effect in the editable installation.
After Rust changes, rebuild the native extension:

```sh
make rebuild
```

## Check changes

```sh
make lint
make verify
```

`make verify` checks the installed package, fresh-cache preparation, offline use,
and the conversion corpus. It downloads pinned catalogs. To also check textured
rendering after online preparation:

```sh
uv run --locked python scripts/verify_package.py --visuals
```

Keep behavior checks small. Keep the public Python facade, native signatures,
type stubs, and docs consistent. To build and check distribution files, run
`make build` and `make check-dist`; check the built package in a separate environment.

## Update documentation

The API reference is generated from Python signatures and docstrings and WASM
declarations. Install the [WASM build prerequisites](docs/guides/getting-started-wasm.md#build),
then run:

```sh
make docs
make docs-check
```

For data changes, keep source records and notices with imported data. The
[source overview](docs/reference/sources.md) links to pins, regeneration commands,
and attribution records. 
