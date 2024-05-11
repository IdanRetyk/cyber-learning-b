
import math

def ex8():
    if len(sum) > 0:
        
        sum = list[0]
        for i in list[1::]:
            sum += i
        return sum



#==============
#       ex9
#===============+++++





# A. donuts
# Given an int count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    my_string = "Number of donuts: "
    if count >= 10:
        my_string += "many"
    else:
        my_string += str(count)
        
    return my_string


# B. both_ends
# Given a string s, return a string made of the first 2
# and the last 2 chars of the original string,
# so 'spring' yields 'spng'. However, if the string length
# is less than 2, return instead the empty string.
def both_ends(s):
    if len(s) > 2:
        return s[0] + s[1] + s[len(s) - 2] + s[len(s) - 1]
    else:
        return ""


# C. fix_start
# Given a string s, return a string
# where all occurences of its first char have
# been changed to '*', except do not change
# the first char itself.
# e.g. 'babble' yields 'ba**le'
# Assume that the string is length 1 or more.
# Hint: s.replace(stra, strb) returns a version of string s
# where all instances of stra have been replaced by strb.
def fix_start(s):
    return s[0] + s[1::].replace(s[0], '*')


# D. MixUp
# Given strings a and b, return a single string with a and b separated
# by a space '<a> <b>', except swap the first 2 chars of each string.
# e.g.
#   'mix', pod' -> 'pox mid'
#   'dog', 'dinner' -> 'dig donner'
# Assume a and b are length 2 or more.
def mix_up(a, b):
    stra = b[0] + b[1] + a[2::]
    strb = a[0] + a[1] + b[2::]
    return stra + " " + strb






#==============
#       ex10
#===============+++++

# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    if len(s) >= 3:
        if s[len(s) - 3:len(s)] == "ing":
            s += "ly"
        else:
            s += "ing"
    return s


# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
    not_index = -1
    bad_index = -1
    new_str = s
    for i in range(len(s) - 2):
        if s[i] + s[i+1] + s[i+2] == "not" and not_index == -1:
            not_index = i
        if s[i] + s[i+1] + s[i+2] == "bad" and bad_index == -1:
            bad_index = i
    
    if not_index < bad_index:
        new_str = s[:not_index] + "good" + s[bad_index + 3::]
    return new_str


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    aFront = a[0:len(a)//2]
    bFront = b[0:len(b)//2]
    aBack = a[len(a)//2:]
    bBack = b[len(b)//2:]
    if len(a) % 2 == 1:
        aFront += aBack[0]
        aBack = aBack[1:]
    
    if len(b) % 2 == 1:
       bFront += bBack[0]
       bBack = bBack[1:]
    
    
    return aFront + bFront + aBack + bBack


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.



 


#==============
#       ex11
#===============+++++





# A. match_ends
# Given a list of strings, return the count of the number of
# strings where the string length is 2 or more and the first
# and last chars of the string are the same.
# Note: python does not have a ++ operator, but += works.
def match_ends(words):
    count = 0
    for st in words:
        if len(st) > 1 and st[0] == st[len(st) - 1]:
            count += 1
    return count


# B. front_x
# Given a list of strings, return a list with the strings
# in sorted order, except group all the strings that begin with 'x' first.
# e.g. ['mix', 'xyz', 'apple', 'xanadu', 'aardvark'] yields
# ['xanadu', 'xyz', 'aardvark', 'apple', 'mix']
# Hint: this can be done by making 2 lists and sorting each of them
# before combining them.
def front_x(words):
    newList = []
    nonXList = []
    for st in words:
        if st[0] == 'x':
            newList.append(st)
        else:
            nonXList.append(st)
    newList.sort()
    nonXList.sort()
    
    for st in nonXList:
        newList.append(st)
    
    return newList



# C. sort_last
# Given a list of non-empty tuples, return a list sorted in increasing
# order by the last element in each tuple.
# e.g. [(1, 7), (1, 3), (3, 4, 5), (2, 2)] yields
# [(2, 2), (1, 3), (3, 4, 5), (1, 7)]
# Hint: use a custom key= function to extract the last element form each tuple.
def sort_last(tuples):
  # +++your code here+++
    return




# Additional basic list exercises

# D. Given a list of numbers, return a list where
# all adjacent == elements have been reduced to a single element,
# so [1, 2, 2, 3] returns [1, 2, 3]. You may create a new list or
# modify the passed in list.
def remove_adjacent(nums):
    prev = ""
    for num in nums:
        if nums[len(nums) - 1] == nums[len(nums) - 2]:
            del nums[len(nums) - 1]
        if num == prev:
            nums.remove(num)
        prev = num
    
    return nums


# E. Given two lists sorted in increasing order, create and return a merged
# list of all the elements in sorted order. You may modify the passed in lists.
# Ideally, the solution should work in "linear" time, making a single
# pass of both lists.
def linear_merge(list1, list2):
    newList = []
    index1 = 0
    index2 = 0
    while (index1 < len(list1) and index2 < len(list2)):
        if list1[index1] > list2[index2]:
            newList.append(list2[index2])
            index2 += 1
        else:
            newList.append(list1[index1])
            index1 += 1
    if len(list1) > len(list2):
        newList += list1[index1:]
    else:
        newList+= list2[index2:]
    return newList

# Note: the solution above is kind of cute, but unforunately list.pop(0)
# is not constant time with the standard python list implementation, so
# the above is not strictly linear time.
# An alternate approach uses pop(-1) to remove the endmost elements
# from each list, building a solution list which is backwards.
# Then use reversed() to put the result back in the correct order. That
# solution works in linear time, but is more ugly.


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print(f'{prefix} got: {repr(got)} expected: {repr(expected)}')


# Calls the above functions with interesting inputs.
def main():
  print ('remove_adjacent')
  test(remove_adjacent([1, 2, 2, 3]), [1, 2, 3])
  test(remove_adjacent([2, 2, 3, 3, 3]), [2, 3])
  test(remove_adjacent([]), [])

  print
  print('linear_merge')
  test(linear_merge(['aa', 'xx', 'zz'], ['bb', 'cc']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'xx'], ['bb', 'cc', 'zz']),
       ['aa', 'bb', 'cc', 'xx', 'zz'])
  test(linear_merge(['aa', 'aa'], ['aa', 'bb', 'bb']),
       ['aa', 'aa', 'aa', 'bb', 'bb'])


if __name__ == '__main__':
  main()



def circle_area(radius):return radius * math.pi() * math.pi()
def triangle_area(ray1, ray2, angle): return ray1 * ray2 * math.sin(angle)
def angle(m1,m2): return math.atan(m1) - math.atan(m2)