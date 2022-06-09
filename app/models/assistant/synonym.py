from typing import Optional, List, Dict, Any


class EntryDisplay:
    def __init__(
            self,
            title: str,
            description: Optional[str] = None,
            footer: Optional[str] = None
    ):
        self.title = title
        self.description = description
        self.footer = footer

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        return cls(
            title=payload['title'],
            description=payload.get('description'),
            footer=payload.get('footer')
        )

# TODO(): Add EntryDisplay.Image / EntryDisplay.OpenURL


class Entry:
    def __init__(
            self,
            name: str,
            synonyms: List[str],
            display: Optional[EntryDisplay] = None
    ):
        self.name = name
        self.synonyms = synonyms
        self.display = display

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        display = None
        if 'display' in payload:
            display = payload['display']

        return cls(
            name=payload['name'],
            synonyms=payload['synonyms'],
            display=display,
        )


class SynonymType:
    def __init__(self, entries: List[Entry]):
        self.entries = entries

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]):
        return cls(
            entries=[Entry.from_payload(x) for x in payload['entries']]
        )