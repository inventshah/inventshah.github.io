"""
Sachin Shah
December 2021

Compiler script for personal website
"""

import json
import os
from typing import Dict, List

from bs4 import BeautifulSoup  # type: ignore


def entry_to_html(
    name: str, desc: str, links: List[Dict[str, str]], image: str, meta: str = ""
) -> str:
    def prefix() -> str:
        return f"[{meta}] " if meta else ""

    link = '[<a href="{link}" target="_blank">{label}</a>]'

    link_tags = "\n".join(
        link.format(link=link_info["link"], label=link_info["label"].lower())
        for link_info in links
    )

    return f"""
        <div class="entry">
            <img class='icon' src={image!r} alt={os.path.basename(image)!r} loading="lazy"/>
            <div>
                <strong>{prefix() + name}</strong>
                <br/>
                {desc}
                {link_tags}
            </div>
        </div>
        """


with open("header.html", "r") as f:
    header = BeautifulSoup(f, features="html.parser")

with open("projects.json") as f:
    data: Dict[str, List[dict]] = json.load(f)

html = "<hr>".join(
    (
        f'<h3 style="color: #1d73db">{category}</h3>{"".join(entry_to_html(**entry) for entry in raw_entries)}'
        for category, raw_entries in data.items()
    )
)

html = BeautifulSoup(html, features="html.parser")
header.body.append(html)

with open("index.html", "w") as f:
    f.write(str(header))
