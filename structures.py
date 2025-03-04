from dataclasses import dataclass


@dataclass
class WikiPage:
    name: str
    url: str
    content: str