import re
from pathlib import Path
from shutil import copyfile, rmtree
from urllib.parse import urljoin, urlsplit
from zipfile import ZIP_DEFLATED, ZipFile

import tomllib
from markdown import Markdown

ROOT = Path(__file__).resolve().parents[1]


def pages(navigation):
    for entry in navigation:
        for value in entry.values():
            if isinstance(value, list):
                yield from pages(value)
            elif value.endswith(".md") and not urlsplit(value).scheme:
                yield value


def page_url(path, site_url):
    target = path.parent if path.name == "index.md" else path.with_suffix("")
    return urljoin(site_url, "" if target == Path(".") else target.as_posix() + "/")


def documentation(config):
    site_url = config["site_url"].rstrip("/") + "/"
    snippets = Markdown(
        extensions=["pymdownx.snippets"],
        extension_configs={"pymdownx.snippets": {"base_path": [str(ROOT)], "check_paths": True}},
    ).preprocessors["snippet"]
    sections = []
    contents = []
    for name in dict.fromkeys(pages(config["nav"])):
        path = (ROOT / "docs" / name).resolve()
        relative = path.relative_to(ROOT / "docs")
        url = page_url(relative, site_url)
        body = re.sub(r"\A---\n.*?\n---\n", "", path.read_text(encoding="utf-8"), flags=re.S)
        body = "\n".join(snippets.run(body.splitlines()))
        base = urljoin(site_url, relative.as_posix())

        def link(match, base=base):
            target = match[1]
            if urlsplit(target).scheme or target.startswith("//"):
                return match[0]
            resolved = urlsplit(urljoin(base, target))
            target_path = resolved.path
            if target_path.endswith("/index.md"):
                target_path = target_path.removesuffix("index.md")
            elif target_path.endswith(".md"):
                target_path = target_path.removesuffix(".md") + "/"
            return f"]({resolved._replace(path=target_path).geturl()})"

        chunks = re.split(r"(^```.*?^```[^\n]*)", body, flags=re.M | re.S)
        for index in range(0, len(chunks), 2):
            chunk = re.sub(r"^</?(?:div|details|summary)\b[^\n]*\n?", "", chunks[index], flags=re.M)
            chunk = re.sub(r"(?<=\))\{\s*\.[^}\n]*\}", "", chunk)
            chunks[index] = re.sub(r"\]\(([^\s)]+)\)", link, chunk)
        body = "".join(chunks).strip()
        title = re.search(r"^# (.+)$", body, re.M)[1]
        contents.append(f"- [{title}]({url})")
        sections.append(f"Source: {url}\n\n{body}")
    header = (
        f"# {config['site_name']} documentation\n\n"
        f"> {config['site_description']}\n\n"
        "Generated from the website's Markdown sources. Includes quickstarts, SDK chapters, "
        "examples, and API references. Check installed package signatures when versions differ.\n\n"
        "## Contents\n\n" + "\n".join(contents)
    )
    return header + "\n\n---\n\n" + "\n\n---\n\n".join(sections) + "\n"


def main() -> None:
    destination = ROOT / "docs/examples/downloads"
    if destination.exists():
        rmtree(destination)
    destination.mkdir(parents=True)
    sources = sorted((ROOT / "examples").glob("*.py"))
    sources.extend(sorted((ROOT / "examples").glob("*.json")))
    sources.extend([ROOT / "examples/build.rs", ROOT / "LICENSE"])
    with ZipFile(destination / "examples.zip", "w", compression=ZIP_DEFLATED) as archive:
        for source in sources:
            copyfile(source, destination / source.name)
            archive.write(source, source.name)
    print("Prepared example source downloads and examples.zip")
    config = tomllib.loads((ROOT / "zensical.toml").read_text(encoding="utf-8"))["project"]
    (ROOT / "docs/llms.txt").write_text(documentation(config), encoding="utf-8")
    print("Generated llms.txt from the published documentation")


if __name__ == "__main__":
    main()
