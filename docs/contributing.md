# Contributing

Library changes, examples, and data updates use the repository checkout.
If you are only editing documentation, you can skip the Rust build and follow
the website setup below.

## Setup

Install [uv](https://docs.astral.sh/uv/) and [Rust](https://rustup.rs/), then run:

```sh
git clone https://github.com/tiltedlabs-ai/mcschemora.git
cd mcschemora
make setup
```

The checkout pins Python 3.12 and Rust 1.88.0. `make setup` installs the Python
package in editable mode. Changes to the Python facade take effect immediately.
After changing Rust code, rebuild the extension with `make rebuild`.

## Repository layout

| Area | Location |
| --- | --- |
| Python public API and type stubs | `bindings/python/python/mcschemora/` |
| Native Python bindings | `bindings/python/src/` |
| Rust implementation | `src/` |
| Browser bindings | `bindings/wasm/` |
| Runnable examples | `examples/` |
| Documentation | `docs/` |
| Data import and verification scripts | `scripts/` |

Keep public signatures, type stubs, docstrings, and examples consistent when
changing an API. Fix every caller affected by the change.

## Checks

```sh
make lint
make verify
```

`make lint` checks Rust formatting and Clippy, plus Python formatting and Ruff.
`make verify` checks the installed package, fresh-cache preparation, offline
use, and the conversion corpus. It downloads pinned catalogs.

For textured rendering, also run:

```sh
uv run --locked scripts/verify_package.py --visuals
```

To build and check distributions, use `make build` and `make check-dist`.
Install the resulting wheel into a clean environment outside the checkout and
run the relevant examples there.

## Documentation

Install uv and Python 3.12, then run from the checkout:

```sh
make docs-serve
```

Open `http://localhost:8000`. The command installs the docs dependency group,
publishes example source downloads, and starts Zensical. Stop it with Ctrl+C.
Use `make docs-build` to write the static site into `site/`.

Example code blocks include files from `examples/`, so edit the source file
to change the code readers see. During a running preview, rerun
`make docs-prepare` after editing an example to refresh its download. Regenerate
published artifacts in `docs/assets/examples/` with the script's default parameters,
and check its diagnostics before replacing an image or schematic.

Preparation also generates `docs/llms.txt` from the Markdown pages in
`zensical.toml` navigation order. It expands source snippets, removes frontmatter
and layout wrappers, and turns relative links into website URLs. This generated
file is ignored by Git and copied into the site. To update it during a preview,
edit the original pages or scripts and run `make docs-prepare`.
`make docs-build` refreshes it before each build, and `make docs-serve` refreshes
it at startup. The API reference has a separate generation command below.

The documentation workflow builds pull requests and deploys pushes to `main`
on GitHub Pages. For initial setup, choose **GitHub Actions** as the repository's
Pages publishing source. Example changes also trigger that workflow.

## API reference

Python reference pages come from signatures and docstrings. The browser
reference comes from wasm-bindgen declarations. Install the
[browser build prerequisites](languages/wasm.md#build), then run:

```sh
make docs
make docs-check
```

Commit the generated Markdown with the code change. A normal website build
uses those checked-in pages and does not compile the package or WASM.

## Data sources

Keep source records and notices with imported data. The
[source overview](reference/sources.md) links to the pinned revisions,
regeneration commands, and asset terms. Regenerate affected outputs and check
that the package still includes its attribution files.

Open an [issue](https://github.com/tiltedlabs-ai/mcschemora/issues) for a bug or
proposed change, or submit a
[pull request](https://github.com/tiltedlabs-ai/mcschemora/pulls) with the change
and the checks you ran.
