
from collections import deque

def trap( height: list[int]) -> int:
        
        
    max_ = 0,0 # Value, Index

    for i in range(len(height)):
        if max_[0] < height[i]:
            max_ = height[i], i
    
    _,max_index = max_

    count = 0

    left_max = 0,0 # Height of heighest build on the left.
    for i in range(max_index):
        if left_max[0] < height[i]:
            left_max = height[i], i
        else:
            count += left_max[0] - height[i]
    
    
    for i in range(7,3,-1):
        print(i)
    
    return count


nums1 = [1,2,3,4,5,6]


print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))
print(nums1)
