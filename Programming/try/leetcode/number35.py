def number35(nums, target):
    left = 0
    right = len(nums)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif target < nums[mid]:
            left = mid - 1
        else:
            right = mid + 1
    return None


nums = [1, 3, 5, 7]
target = 5
print(number35(nums, target))
