# Implementation Overview

This Python script employs the merge sort technique to sort a list of integers in ascending order. The merge sort technique is a divide and conquer algorithm that involves recursively splitting the list into two halves until each subset has only one element and then merging those subsets in a manner which results in a sorted list.

The script is composed of two main functions - `mergeSort()` and `merge()`. The `mergeSort()` function is responsible for recursively dividing the input list into two halves. The `merge()` function is then invoked to take care of the actual process of merging the halves into a sorted list.

# Function Signature

1. `mergeSort(arr: List[int]) -> List[int]`
2. `merge(arr: List[int], left_half: List[int], right_half: List[int]) -> List[int]`

# Parameters

1. `mergeSort(arr: List[int]) -> List[int]`

- arr: A list of integers that is to be sorted.

2. `merge(arr: List[int], left_half: List[int], right_half: List[int]) -> List[int]`

- arr: A list of integers that is to be sorted.
- left_half: The left half of the 'arr' list.
- right_half: The right half of the 'arr' list.

# Return Value

Both the `mergeSort()` and `merge()` functions return the sorted list of integers. The `merge()` function also modifies the original 'arr' list in-place.