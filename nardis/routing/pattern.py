from typing import Any


class RegexPattern:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, path: str) -> dict:
        """Checks if url matches pattern"""
        match = self._match(path)
        if match:
            return match.groupdict()
        return {}

    def match(self, path: str) -> bool:
        return self._match(path) is not None

    def _match(self, path: str) -> Any:
        import re
        return re.search(self.pattern, path)
