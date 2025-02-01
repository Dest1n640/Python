def Two_Sum(nums, target):
    for i in range(len(nums)):
        for q in range(i, len(nums)): 
            if nums[i] + nums[q]  == target:
                return [nums[i], nums[q]]

nums = [int(i) for i in input("Input nums: ").split()]
target = int(input("Input target: "))

print(Two_Sum(nums, target))
