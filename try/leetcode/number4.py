def Median_of_Two_Sorted_Arrays(nums1, nums2):
    m = len(nums1)
    n = len(nums2)
    return (m + n)  / 2

nums1 = [int(i) for i in input().split()]
nums2 = [int(i) for i in input().split()]

print(Median_of_Two_Sorted_Arrays(nums1, nums2))
