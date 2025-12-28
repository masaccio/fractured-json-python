from pathlib import Path
from re import findall
from tomllib import loads as toml_loads

from requests import codes, get

ROOT_DIR = Path(__file__).parent.parent.parent


def check_url(url: str) -> None:
    """Fetch a URL and report status."""
    print(f"Checking: {url}")
    try:
        r = get(url)  # noqa: S113
    except Exception as e:  # noqa: BLE001
        print(f"FAILED: {url} failed with {e}")
    else:
        if r.status_code != codes.ok:
            print("FAILED: {url} returned {r.status_code}")


def test_readme_urls() -> None:
    """Check that all URLs in the README are valid."""
    readme = (ROOT_DIR / "README.md").read_text()
    urls = set(findall(r"\((http.*?)\)", readme))
    for url in urls:
        check_url(url)


def test_package_urls() -> None:
    """Check that all URLs in the README are valid."""
    toml = (ROOT_DIR / "pyproject.toml").read_text()
    project_data = toml_loads(toml)["project"]
    for url in project_data["urls"].values():
        check_url(url)


test_readme_urls()
test_package_urls()
