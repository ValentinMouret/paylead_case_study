from src.utils import batched


def test_batched():
    numbers = range(10)
    batches = batched(numbers, 2)

    assert list(batches) == [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]


def test_batched_odd():
    numbers = range(10)
    batches = batched(numbers, 3)

    assert list(batches) == [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9,)]
