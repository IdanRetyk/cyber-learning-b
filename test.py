

def removeElement(nums: list[int], val: int) -> int:
        
    if len(nums) == 0:
        return 0

    last_index = len(nums) -1

   

    count = 0

    for i in range(len(nums)):
        if nums[last_index] == val:
            last_index -= 1
        if nums[i] == val:
            count += 1
            nums[i] = nums[last_index]
            last_index -= 1
            

    return len(nums) - count



print(removeElement([3,1,3,3,3],3))