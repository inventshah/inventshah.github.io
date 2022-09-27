"""
Sachin Shah
December 2021

Compiler script for personal website
"""
from typing import Dict, List, NamedTuple
import json

from bs4 import BeautifulSoup  # type: ignore


class Entry(NamedTuple):
    name: str
    desc: str
    links: List[Dict[str, str]]
    image: str
    meta: str = ""

    def prefix(self) -> str:
        return f"[{self.meta}] " if self.meta else ""

    def to_html(self) -> str:
        link = '[<a href="{link}" target="_blank">{label}</a>]'

        links = "\n".join(
            link.format(link=link_info["link"], label=link_info["label"].lower())
            for link_info in self.links
        )

        return """
        <li class="entry">
            {image}
            <div>
                <strong>{name}</strong>
                <br/>
                {desc}
                {links}
            </div>
        </li>
        
        """.format(
            name=self.prefix() + self.name,
            desc=self.desc,
            links=links,
            image=f"<img class='icon' src={self.image!r}/>",
        )


with open("header.html", "r") as f:
    header = BeautifulSoup(f, features="html.parser")

with open("projects.json") as f:
    data: Dict[str, List[dict]] = json.load(f)

html = "<hr>".join(
    (
        f'<h3 style="color: #1d73db">{category}</h3>{"".join(Entry(**entry).to_html() for entry in raw_entries)}'
        for category, raw_entries in data.items()
    )
)

html = BeautifulSoup(html, features="html.parser")
header.ul.append(html)

with open("index.html", "w") as f:
    f.write(str(header))
