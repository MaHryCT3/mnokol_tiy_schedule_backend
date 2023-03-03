from typing import TypeVar

T = TypeVar('T')


def singleton(cls: T) -> T:
    instances = {}

    def getinstance(*args, **kwargs) -> T:
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
