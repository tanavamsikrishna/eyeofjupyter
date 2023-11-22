from typing import Any


class KeyValueCache(dict):
    def __init__(self) -> None:
        super().__init__()
        self.cache = {}

    def __getitem__(self, __key: Any) -> Any:
        return super().__getitem__(__key)

    def __setitem__(self, __key: Any, __value: Any) -> None:
        return super().__setitem__(__key, __value)
