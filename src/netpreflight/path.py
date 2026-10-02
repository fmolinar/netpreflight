PathSegment = str | int
# alias for a path segment, which can be either a string (for dictionary keys) or an integer (for list indices)
Path = tuple[PathSegment, ...]


class PathNotFoundError(Exception):
    """Raised when a path is not found in a nested dictionary."""


def get_path(data: object, path: Path) -> object:
    """Get a value from a nested dictionary using a path of keys.

    Args:
        data (dict): The nested dictionary to search.
        path (tuple): A tuple of keys representing the path to the desired value.

    Returns:
        object: The value found at the specified path.

    Raises:
        PathNotFoundError: If any key in the path is not found in the dictionary.
    """
    current = data

    for segment in path:
        # The isinstance() function is a built-in Python function used to check if an object belongs to a specific class or data type, or a subclass of it.
        if isinstance(current, dict) and isinstance(segment, str):
            if segment not in current:
                raise PathNotFoundError(f"Path not found: {path!r}")

            current = current[segment]
            continue

        if isinstance(current, list) and isinstance(segment, int):
            if segment < 0 or segment >= len(current):
                raise PathNotFoundError(f"Path not found: {path!r}")

            current = current[segment]
            continue
        raise PathNotFoundError(f"Path not found: {path!r}")
    return current
