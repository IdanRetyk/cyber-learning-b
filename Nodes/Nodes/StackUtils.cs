using System;
using System.Collections.Generic;

namespace Nodes
{
    class StackUtils<T>
    {
        public static Stack<T> CreateStackFromArray(T[] arr)
        {
            Stack<T> stack = new Stack<T>();
            for (int i = 0; i < arr.Length; i++)
            {
                stack.Push(arr[i]);
            }
            return stack;
        }
        public static void SpillOn(Stack<T> from, Stack<T> to)
        {
            while (!from.IsEmpty())
            {
                to.Push(from.Pop());
            }
            Reverse(to);
        }
        public static Stack<T> Clone(Stack<T> org)
        {
            Stack<T> clone = new Stack<T>();
            Stack<T> tempStack = new Stack<T>();

            while (!org.IsEmpty())
            {
                T value = org.Pop();
                tempStack.Push(value);
                clone.Push(value);
            }

            while (!tempStack.IsEmpty())
            {
                org.Push(tempStack.Pop());
            }

            Reverse(clone);

            return clone;
        }
        public static int SizeRec<T>(Stack<T> org)
        {
            if (org.IsEmpty())
            {
                return 0;
            }
            else
            {
                T element = org.Pop();
                int sizeOfRest = SizeRec(org);
                org.Push(element);
                return 1 + sizeOfRest;
            }
        }
        public static int SizeNotRec(Stack<T> org)
        {
            Stack<T> TempStack = new Stack<T>();
            int cnt = 0;
            while (!org.IsEmpty())
            {
                TempStack.Push(org.Pop());
                cnt++;
            }
            for (int i = cnt - 1; i >= 0; i--)
            {
                org.Push(TempStack.Pop());
            }
            return cnt;
        }
        public static int Sum(Stack<int> s)
        {
            Stack<int> Clone = StackUtils<int>.Clone(s);
            int sum = 0;
            while (!Clone.IsEmpty())
            {
                sum += Clone.Pop();
            }
            return sum;
        }
        public static bool IsExist(Stack<int> s, int num)
        {
            Stack<int> Clone = StackUtils<int>.Clone(s); ;
            while (!Clone.IsEmpty())
            {
                if (Clone.Pop() == num)
                    return true;
            }
            return false;
        }
        public static bool IsSorted(Stack<int> s)
        {
            int prev = s.Pop();
            if (s.IsEmpty())
                return true;
            while (!s.IsEmpty())
            {
                int cur = s.Pop();
                if (cur > prev)
                    return false;
                prev = cur;
            }
            return true;
        }
        public static void InsertAtBottom(Stack<T> stack, T value)
        {
            Stack<T> tempStack = new Stack<T>();

            while (!stack.IsEmpty())
            {
                tempStack.Push(stack.Pop());
            }

            stack.Push(value);

            while (!tempStack.IsEmpty())
            {
                stack.Push(tempStack.Pop());
            }
        }

        public static void SwapFromTopToBottom(Stack<T> stack)
        {
            T top = stack.Pop();
            InsertAtBottom(stack, top);
        }
        public static int FindMaxInStack(Stack<int> s)
        {
            Stack<int> Clone = StackUtils<int>.Clone(s);
            if (Clone.IsEmpty())
                throw new Exception("stack is empty so there is no max value");
            int curMax = Clone.Pop();
            while (!Clone.IsEmpty())
            {
                curMax = Math.Max(Clone.Pop(), curMax);
            }
            return curMax;
        }
        public static int FindMaxInStackndRemoveIt(Stack<int> s)
        {
            int max = int.MinValue;
            Stack<int> tempStack = new Stack<int>();

            while (!s.IsEmpty())
            {
                int current = s.Pop();
                max = Math.Max(current, max);
                tempStack.Push(current);
            }

            while (!tempStack.IsEmpty())
            {
                int current = tempStack.Pop();
                if (current != max)
                {
                    s.Push(current);
                }
            }

            return max;
        }
        public static void InsertAtN(Stack<T> stack, int index, T value)
        {
            Stack<T> tempStack = new Stack<T>();
            int cnt = 0;

            while (cnt < index && !stack.IsEmpty())
            {
                tempStack.Push(stack.Pop());
                cnt++;
            }

            stack.Push(value);

            while (!tempStack.IsEmpty())
            {
                stack.Push(tempStack.Pop());
            }
        }
        public static T RemoveFromBottom(Stack<T> stack)
        {
            Stack<T> tempStack = new Stack<T>();
            int cnt = 0;

            while (!stack.IsEmpty())
            {
                tempStack.Push(stack.Pop());
                cnt++;
            }

            T bottom = tempStack.Pop();

            for (int i = cnt - 2; i >= 0; i--)
            {
                stack.Push(tempStack.Pop());
            }

            return bottom;
        }
        public static void MoveBottomHead(Stack<T> stack)
        {
            T bottom = StackUtils<T>.RemoveFromBottom(stack);
            stack.Push(bottom);
        }
        public static void RemoveAtN(Stack<T> stack, int index)
        {
            Stack<T> tempStack = new Stack<T>();
            int cnt = 0;

            while (cnt < index && !stack.IsEmpty())
            {
                tempStack.Push(stack.Pop());
                cnt++;
            }

            if (!stack.IsEmpty())
            {
                stack.Pop();
            }

            while (!tempStack.IsEmpty())
            {
                stack.Push(tempStack.Pop());
            }
        }
        public static void Reverse(Stack<T> stack)
        {
            Stack<T> tempStack = new Stack<T>();
            Stack<T> tempStack2 = new Stack<T>();
            while (!stack.IsEmpty())
            {
                tempStack.Push(stack.Pop());
            }

            while (!tempStack.IsEmpty())
            {
                tempStack2.Push(tempStack.Pop());
            }
            while (!tempStack2.IsEmpty())
            {
                stack.Push(tempStack2.Pop());
            }
        }
        public static Stack<T> sort(Stack<T> stack)
        {
            Stack<T> sortedStack = new Stack<T>();
            while (!stack.IsEmpty())
            {
                T current = stack.Pop();
                while (!sortedStack.IsEmpty() && Comparer<T>.Default.Compare(current, sortedStack.Top()) > 0)
                {
                    stack.Push(sortedStack.Pop());
                }
                sortedStack.Push(current);
            }
            return sortedStack;
        }

    }
}



