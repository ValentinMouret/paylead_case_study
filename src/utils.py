from itertools import islice
from typing import Iterable, TypeVar

T = TypeVar("T")


def batched(iterable: Iterable[T], n) -> Iterable[tuple[T, ...]]:
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch
