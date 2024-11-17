## Implementation Overview
This implementation provides a clean and efficient solution for performing merge sort on a list of integers in Python. The `merge_sort` function recursively divides the input list into smaller sublists until each sublist contains only one element. Then, the `merge` function merges these sublists in a sorted manner. The final sorted list is returned.

## Function Signature
```python
def merge(left: List[int], right: List[int]) -> List[int]:
def merge_sort(arr: List[int]) -> List[int]:
```

## Parameters
- `left`: List of integers representing the left sublist to merge.
- `right`: List of integers representing the right sublist to merge.
- `arr`: List of integers to be sorted using merge sort.

## Return Value
- `merge`: Returns a sorted list of integers after merging the left and right sublists.
- `merge_sort`: Returns a sorted list of integers after performing merge sort on the input list.