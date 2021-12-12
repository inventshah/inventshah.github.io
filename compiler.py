"""
Sachin Shah
December 2021

Compiler script for personal website
"""
from collections import defaultdict
from typing import Dict, List, NamedTuple, Optional, Tuple
import json

from bs4 import BeautifulSoup  # type: ignore


class Entry(NamedTuple):
    name: str
    desc: str
    links: List[Dict[str, str]]
    category: str
    image: Optional[str] = None
    meta: str = ""

    def prefix(self) -> str:
        return "" if not self.meta else f"[{self.meta}] "


def project_entry(entry: Entry) -> Tuple[str, str]:
    link = '[<a href="{link}" target="_blank">{label}</a>]'

    links = "\n".join(
        link.format(link=link_info["link"], label=link_info["label"].lower())
        for link_info in entry.links
    )

    return entry.category, """
    <li class="entry">
        {image}
        <div>
            <strong>{name}</strong>
            <br/>
            {desc}
            {links}
        </div>
    </li>
    <br/>
    """.format(
        name=entry.prefix() + entry.name,
        desc=entry.desc,
        links=links,
        image=f"<img class='icon' src={entry.image!r}/>" if entry.image else "",
    )


with open("header.html", "r") as f:
    header = BeautifulSoup(f, features="html.parser")


with open("projects.json") as f:
    data = json.load(f)

data = (Entry(**entry) for entry in data)
data = map(project_entry, data)

categories = defaultdict(str)
for category, html in data:
    categories[category] += html

html = "<hr>".join(
    (f"<h3>{category}</h3>{content}" for category, content in categories.items())
)

html = BeautifulSoup(html, features="html.parser")
header.ul.append(html)

with open("index.html", "w") as f:
    f.write(str(header))
