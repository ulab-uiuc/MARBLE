# README.md

## Implementation Overview
This implementation provides the Python code for a merge sort algorithm. The merge sort algorithm is a divide and conquer algorithm that divides a list into halves, sorts them and then merges them. This implementation contains two functions: `merge_sort` and `merge`.

The `merge_sort` function is the main function that takes in a list of integers and returns the sorted list. It recursively divides the input list into two halves until we reach the base case where the list contains only one or zero elements. Then, it calls the `merge` function to merge the sorted halves. 

The `merge` function merges two sorted lists into one sorted list. It does so by comparing the smallest elements of the two lists and pushing the smallest one into the result list. This is done until all elements of the two lists are in the result list.

## Function Signature
```python
def merge_sort(array: List[int]) -> List[int]:
    # function body

def merge(left: List[int], right: List[int]) -> List[int]:
    # function body
```

## Parameters
1. `merge_sort` function:
    - `array`: The list of integers to be sorted.
2. `merge` function:
    - `left`: The left half of the list.
    - `right`: The right half of the list.

## Return Value
1. `merge_sort` function:
    - Returns the sorted list.
2. `merge` function:
    - Returns the merged sorted list.