from dataclasses import dataclass

@dataclass
class Entry:
    title: str
    url: str
    question: str
    embedding: np.ndarray

@dataclass
class Database:
    entries: list[Entry]

@dataclass
class WikiPage:
    name: str
    url: str
    content: str
