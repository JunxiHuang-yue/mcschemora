"""Check release metadata and required files without importing the native module."""

import argparse
import re
import tarfile
from email.parser import BytesParser
from pathlib import Path
from zipfile import ZipFile

import tomllib

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "mcschemora"
NOTICES = (
    "LICENSE",
    "NOTICE",
    "block-models/LICENSE",
    "block-models/SOURCE.md",
    "entity-models/SOURCE.md",
    "entity-models/ATTRIBUTION.json",
    "wiki-sprites/SOURCE.md",
    "wiki-sprites/ATTRIBUTION.json",
    "runtime-data/SOURCE.md",
    "catalogs/SOURCE.md",
    "recipes/SOURCE.md",
    "material-values/SOURCE.md",
)


def check_metadata(content: bytes, version: str) -> None:
    metadata = BytesParser().parsebytes(content)
    assert metadata["Name"] == PACKAGE, metadata["Name"]
    assert metadata["Version"] == version, metadata["Version"]
    assert metadata["Requires-Python"] == ">=3.10", metadata["Requires-Python"]
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    assert metadata["License-Expression"] == project["license"], metadata["License-Expression"]
    assert metadata["Description-Content-Type"].startswith("text/markdown")
    description = metadata.get_payload(decode=True).decode("utf-8")
    assert description.rstrip() == (ROOT / project["readme"]).read_text().rstrip(), (
        "Package description differs from the project README"
    )
    assert any("tiltedlabs-ai/mcschemora" in url for url in metadata.get_all("Project-URL", []))
    assert "whuang37/schemora" not in content.decode()


def check_wheel(path: Path, version: str) -> None:
    with ZipFile(path) as wheel:
        names = set(wheel.namelist())
        metadata_files = [name for name in names if name.endswith(".dist-info/METADATA")]
        assert len(metadata_files) == 1, metadata_files
        check_metadata(wheel.read(metadata_files[0]), version)
        config = tomllib.loads((ROOT / "pyproject.toml").read_text())
        python_source = ROOT / config["tool"]["maturin"]["python-source"] / PACKAGE
        for name in ("__init__.py", "_core.pyi", "py.typed"):
            assert f"{PACKAGE}/{name}" in names, name
            assert wheel.read(f"{PACKAGE}/{name}") == (python_source / name).read_bytes(), name
        assert any(
            name.startswith(f"{PACKAGE}/_core") and name.endswith((".so", ".pyd")) for name in names
        ), "Missing native extension"
        for name in NOTICES:
            assert f"{PACKAGE}/licenses/{name}" in names, name
        assert not any("__pycache__" in name or name.endswith(".pyc") for name in names)


def check_source(path: Path, version: str) -> None:
    with tarfile.open(path) as source:
        files = {member.name: member for member in source.getmembers() if member.isfile()}
        prefix = f"{PACKAGE}-{version}/"
        assert all(name.startswith(prefix) for name in files), "Unexpected source archive root"
        names = {name.removeprefix(prefix) for name in files}
        metadata = source.extractfile(files[prefix + "PKG-INFO"])
        assert metadata is not None
        check_metadata(metadata.read(), version)
        required = {
            "Cargo.toml",
            "Cargo.lock",
            "LICENSE",
            "pyproject.toml",
            "bindings/python/Cargo.toml",
            "bindings/python/build.rs",
            "bindings/python/NOTICE",
            "README.md",
            "data/block-models/SOURCE.md",
            "data/entity-models/SOURCE.md",
            "data/wiki-sprites/SOURCE.md",
            "data/cost/java/values/SOURCE.md",
            "src/catalog/data/SOURCE.md",
            "src/catalog/recipes/SOURCE.md",
            "src/catalog/storage/native/SOURCE.md",
        }
        config = source.extractfile(files[prefix + "pyproject.toml"])
        assert config is not None
        python_source = tomllib.loads(config.read().decode())["tool"]["maturin"]["python-source"]
        required.update(
            f"{python_source}/mcschemora/{name}"
            for name in (
                "__init__.py",
                "_core.pyi",
                "py.typed",
            )
        )
        for rust in (ROOT / "src").rglob("*.rs"):
            required.add(rust.relative_to(ROOT).as_posix())
            for relative in re.findall(
                r'include_(?:str|bytes)!\(\s*"([^"]+)"\s*\)', rust.read_text()
            ):
                required.add((rust.parent / relative).resolve().relative_to(ROOT).as_posix())
        missing = sorted(required - names)
        assert not missing, f"Missing source inputs: {missing}"
        for name in required:
            if name.startswith(("src/", "data/")):
                content = source.extractfile(files[prefix + name])
                assert content is not None
                assert content.read() == (ROOT / name).read_bytes(), f"Stale source input: {name}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    version = tomllib.loads((ROOT / "Cargo.toml").read_text())["workspace"]["package"]["version"]
    wheels = sorted(args.directory.glob("*.whl"))
    sources = sorted(args.directory.glob("*.tar.gz"))
    assert wheels and len(sources) == 1, "Expected wheels and one source archive"
    for path in wheels:
        check_wheel(path, version)
        print(f"Checked {path.name}")
    check_source(sources[0], version)
    print(f"Checked {sources[0].name}")


if __name__ == "__main__":
    main()
