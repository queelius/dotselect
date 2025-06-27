import re
from typing import Any, Iterable, Optional, List, Union, Dict

_PATH_TOKEN_RE = re.compile(r"(\w+\[.*?\]|\*\*|\*|[\w-]+)")

def _coerce_value(value_str: str) -> Union[str, int, float, bool, None]:
    """Converts a string from a predicate into a more specific Python type."""
    val_lower = value_str.lower()
    if val_lower == 'true':
        return True
    if val_lower == 'false':
        return False
    if val_lower in ('null', 'none'):
        return None
    try:
        if '.' in value_str:
            return float(value_str)
        return int(value_str)
    except ValueError:
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        return value_str

def _parse_path(path: str) -> List[Dict]:
    """Tokenizes a path string into a list of segments for the traversal engine."""
    segments = []
    parts = re.split(r'\.', path)
    for part in parts:
        match = re.match(r"(\w+)\[(\w+)=([^\]]+)\]", part)
        if match:
            field, key, value_str = match.groups()
            coerced_value = _coerce_value(value_str)
            segments.append({'type': 'predicate', 'field': field, 'key': key, 'value': coerced_value})
        elif part == '*':
            segments.append({'type': 'wildcard'})
        elif part == '**':
            segments.append({'type': 'descendant'})
        elif part.isdigit():
            segments.append({'type': 'index', 'value': int(part)})
        else:
            segments.append({'type': 'key', 'value': part})
    return segments

def _traverse(data: Any, segments: List[Dict]) -> Iterable[Any]:
    """A powerful traversal engine that understands all segment types."""
    if not segments:
        yield data
        return

    head, *tail = segments

    if head['type'] == 'descendant':
        yield from _traverse(data, tail)
        if isinstance(data, dict):
            for value in data.values():
                yield from _traverse(value, [head] + tail)
        elif isinstance(data, list):
            for item in data:
                yield from _traverse(item, [head] + tail)

    elif head['type'] == 'key':
        if isinstance(data, dict) and head['value'] in data:
            yield from _traverse(data[head['value']], tail)

    elif head['type'] == 'index':
        if isinstance(data, list) and -len(data) <= head['value'] < len(data):
            yield from _traverse(data[head['value']], tail)

    elif head['type'] == 'wildcard':
        if isinstance(data, dict):
            for value in data.values():
                yield from _traverse(value, tail)
        elif isinstance(data, list):
            for item in data:
                yield from _traverse(item, tail)

    elif head['type'] == 'predicate':
        field, key, value = head['field'], head['key'], head['value']
        if isinstance(data, dict) and field in data:
            list_to_filter = data.get(field)
            if isinstance(list_to_filter, list):
                for item in list_to_filter:
                    if isinstance(item, dict) and item.get(key) == value:
                        yield from _traverse(item, tail)

class Path:
    """Represents a compiled path using the full dotpath language."""
    def __init__(self, path_str: str):
        self.path_str = path_str
        self._segments = _parse_path(path_str)

    def find_all(self, data: Any) -> Iterable[Any]:
        """Find all values in data that match this path."""
        yield from _traverse(data, self._segments)

    def find_first(self, data: Any) -> Optional[Any]:
        """Find the first value in data that matches this path."""
        try:
            return next(self.find_all(data))
        except StopIteration:
            return None

def find_all(data: Any, path_str: str) -> Iterable[Any]:
    """A convenience function to find all values that match the path string."""
    return Path(path_str).find_all(data)

def find_first(data: Any, path_str: str) -> Optional[Any]:
    """A convenience function to find the first value that matches the path string."""
    return Path(path_str).find_first(data)
