.PHONY: setup rebuild build check-dist verify format lint docs docs-check docs-wasm

setup:
	uv sync --locked

rebuild:
	uv sync --locked --reinstall-package mcschemora

build:
	uv run --locked maturin build --release --locked --sdist --out dist

check-dist:
	uv run --locked python scripts/check_distributions.py dist
	uvx --from 'twine>=6,<7' twine check --strict dist/*

verify:
	uv run --locked python scripts/verify_package.py
	uv run --locked python scripts/verify_conversion.py

docs-wasm:
	npm --prefix bindings/wasm run build

docs: rebuild docs-wasm
	uv run --locked python scripts/generate_docs.py

docs-check: rebuild docs-wasm
	uv run --locked python scripts/generate_docs.py --check

format:
	cargo fmt --all
	uv run --locked ruff format bindings/python/python scripts

lint:
	cargo fmt --all -- --check
	cargo clippy --locked --workspace --all-targets -- -D warnings
	uv run --locked ruff format --check bindings/python/python scripts
	uv run --locked ruff check bindings/python/python scripts
