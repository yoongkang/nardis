from typing import Any


class RegexPattern:
    def __init__(self, pattern):
        self.pattern = pattern

    def parse(self, path: str) -> dict:
        """Get params from the URL"""
        match = self._match(path)
        return match.groupdict()

    def match(self, path: str) -> bool:
        """Checks if path matches pattern"""
        return self._match(path) is not None

    def _match(self, path: str) -> Any:
        import re
        return re.search(self.pattern, path)
