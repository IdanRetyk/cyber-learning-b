
def merge( nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        nums1_ = [num for num in nums1]

        i = 0
        j = 0


        for k in range(len(nums1)):
            if (i == m):
                nums1[k] = nums2[j]
                j += 1
            elif (j == n):
                nums1[k] = nums1_[i]
                i += 1
            elif nums1_[i] < nums2[j]:
                nums1[k] = nums1_[i]
                i += 1
            else:
                nums1[k] = nums2[j]
                j += 1
    
nums1 = [1,2,3,0,0,0]
nums2 = [2,5,6]

merge(nums1,3,nums2,3)

print(nums1)