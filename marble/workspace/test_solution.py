```python
import pytest
from sorting import merge, merge_sort

# Unit Tests
def test_merge_sort():
    assert merge_sort([12, 11, 13, 5, 6, 7]) == [5, 6, 7, 11, 12, 13]
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([4, 3, 2, 1]) == [1, 2, 3, 4]

def test_merge():
    assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge([1, 2, 3], []) == [1, 2, 3]
    assert merge([], [1, 2, 3]) == [1, 2, 3]
    assert merge([], []) == []

# Edge Cases
def test_merge_sort_edge_cases():
    assert merge_sort([]) == []
    assert merge_sort([1]) == [1]
    assert merge_sort([4, 4, 4, 4]) == [4, 4, 4, 4]
    assert merge_sort([1, 1, 2, 2, 3, 3]) == [1, 1, 2, 2, 3, 3]

def test_merge_edge_cases():
    assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge([1, 2, 3], []) == [1, 2, 3]
    assert merge([], [1, 2, 3]) == [1, 2, 3]
    assert merge([], []) == []

# Performance Test
def test_merge_sort_performance(benchmark):
    large_input = [i for i in range(1000, 0, -1)]
    assert benchmark(merge_sort, large_input) == sorted(large_input)

# Error Handling Cases
def test_merge_sort_error_handling():
    with pytest.raises(TypeError):
        merge_sort("invalid input")
    with pytest.raises(TypeError):
        merge_sort(None)

def test_merge_error_handling():
    with pytest.raises(TypeError):
        merge([1, 2, 3], "invalid input")
    with pytest.raises(TypeError):
        merge(None, [1, 2, 3])
```

Run the tests using the following command:
```bash
pytest test_sorting.py
``` 

These tests cover functional correctness, edge cases, performance characteristics, and error handling scenarios for the merge sort algorithm.