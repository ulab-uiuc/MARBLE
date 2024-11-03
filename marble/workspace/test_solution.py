```python
import pytest
from typing import List
from random import randint
from coder1 import mergeSort

def test_mergeSort():
    # Functional tests
    arr = [3, 2, 1, 7, 8, 5]
    assert mergeSort(arr) == sorted(arr)

    arr = [-3, -2, -1, -7, -8, -5]
    assert mergeSort(arr) == sorted(arr)

    arr = [3.5, 2.1, 1.6, 7.8, 8.2, 5.7]
    assert mergeSort(arr) == sorted(arr)

    arr = []
    assert mergeSort(arr) == sorted(arr)

    arr = [3, 2, 2, 7, 8, 8, 5, 5]
    assert mergeSort(arr) == sorted(arr)

    # Edge cases
    arr = [1]
    assert mergeSort(arr) == sorted(arr)

    arr = [randint(0, 100) for _ in range(10000)]
    assert mergeSort(arr) == sorted(arr)

    arr = [i for i in range(10, 0, -1)]
    assert mergeSort(arr) == sorted(arr)

    arr = [i for i in range(10)]
    assert mergeSort(arr) == sorted(arr)

    # Error handling
    arr = ['a', 'b', 'c', 'd', 'e']
    with pytest.raises(TypeError):
        mergeSort(arr)

    arr = None
    with pytest.raises(TypeError):
        mergeSort(arr)

    arr = [1, 2, 3, 'a', 'b', 'c']
    with pytest.raises(TypeError):
        mergeSort(arr)
```