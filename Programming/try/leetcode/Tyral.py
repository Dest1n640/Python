You are given an integer array of length .numsn

A partition is defined as an index where , splitting the array into two non-empty subarrays such that:i0 <= i < n - 1

Left subarray contains indices .[0, i]
Right subarray contains indices .[i + 1, n - 1]
Return the number of partitions where the difference between the sum of the left and right subarrays is even.

 

Example 1:

Input: nums = [10,10,3,7,6]

Output: 4

Explanation:

The 4 partitions are:

[10], with a sum difference of , which is even.[10, 3, 7, 6]10 - 26 = -16
[10, 10], with a sum difference of , which is even.[3, 7, 6]20 - 16 = 4
[10, 10, 3], with a sum difference of , which is even.[7, 6]23 - 13 = 10
[10, 10, 3, 7], with a sum difference of , which is even.[6]30 - 6 = 24
Example 2:

Input: nums = [1,2,2]

Output: 0

Explanation:

No partition results in an even sum difference
