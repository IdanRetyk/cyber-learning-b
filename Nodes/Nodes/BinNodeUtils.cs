using Nodes;
using System;
using System.Collections.Generic;

namespace Nodes
{
    public static class BinNodeUtils
    {
        public static BinNode<T> CreateListFromArray<T>(T[] arr)
        {
            BinNode<T> head = new BinNode<T>(arr[0]);
            BinNode<T> pos = head;
            for (int i = 1; i < arr.Length; i++)
            {
                pos.SetRight(new BinNode<T>(pos, arr[i], null));
                pos = pos.GetRight();   
            }
            return head;
        }


        public static void AddNodeRightEnd<T>(BinNode<T> lst,T val) //add node with the value given at the right end of the list
        {
            while (lst.GetRight() != null)
            {
                lst = lst.GetRight();
            }
            lst.SetRight(new BinNode<T>(lst, val, null));
        }

        public static void AddNodeLeftEnd<T>(BinNode<T> lst, T val)
        {
            while (lst.GetLeft() != null)
            {
                lst = lst.GetLeft();
            }
            lst.SetLeft(new BinNode<T>(null, val, lst));
        }


        public static void AddNodeInSorted(BinNode<int> lst, int val) //lst is a sorted list from left to right
        {
            if (lst.GetValue() > val) //val is smaller than any value in the list
            {
                AddNodeLeftEnd(lst, val);
                return;
            }
            while (lst.GetRight() != null)
            {
                if (lst.GetValue() < val && val <= lst.GetRight().GetValue())
                {
                    lst.SetRight(new BinNode<int>(lst, val, lst.GetRight()));
                }
                lst = lst.GetRight();
            }
            if (lst.GetValue() < val) //val is larget than any value in the list
            {
                AddNodeRightEnd(lst, val);
                return;
            }
        }

        public static void RemoveNode<T>(BinNode<T> lst, int index)
        {
            if (index == 0)
            {
                lst.SetValue(lst.GetRight().GetValue());
                lst.SetRight(lst.GetRight().GetRight());
            }
            else
            {
                for (int i = 0; i + 1 < index; i++)
                {
                    lst = lst.GetRight();
                }
                lst.SetRight(lst.GetRight().GetRight());
            }
        }


        public static bool IsExist<T>(BinNode<T> lst, T val)
        {
            while (lst.GetRight() != null)
            {
                if (lst.GetValue().Equals(val))
                    return true;
                lst = lst.GetRight();
            }
            while (lst.GetLeft() != null)
            {
                if (lst.GetValue().Equals(val))
                    return true;
                lst = lst.GetLeft();
            }
            return false;
        }



        public static BinNode<T> GetLast<T>(BinNode<T> lst)
        {
            while(lst.GetRight() != null)
            {
                lst = lst.GetRight();
            }
            return lst;
        }


        public static bool IsPalindrom(BinNode<char> lst) //o(n)
        {
            BinNode<char> leftPointer = lst;
            while (leftPointer.GetLeft() != null)
            {
                leftPointer = leftPointer.GetLeft();
            }
            BinNode<char> RightPointer = lst;
            while (RightPointer.GetRight() != null)
            {
                RightPointer = RightPointer.GetRight();
            }

            while (leftPointer != RightPointer && leftPointer != null)
            {
                if (leftPointer.GetValue() != RightPointer.GetValue())
                {
                    return false;
                }
                leftPointer = leftPointer.GetRight();
                RightPointer = RightPointer.GetLeft();
            }
            return true;
        }


        public static BinNode<T> GetMiddle<T>(BinNode<T> lst) //o(n)
        {
            BinNode<T> leftPointer = lst;
            while (leftPointer.GetLeft() != null)
            {
                leftPointer = leftPointer.GetLeft();
            }
            BinNode<T> RightPointer = lst;
            while (RightPointer.GetRight() != null)
            {
                RightPointer = RightPointer.GetRight();
            }

            while (leftPointer != RightPointer)
            {
                leftPointer = leftPointer.GetRight();
                RightPointer = RightPointer.GetLeft();
            }
            return leftPointer;
        }


        public static BinNode<int> InputArrayReverse() //o(n)
        {
            int input = int.Parse(Console.ReadLine());
            BinNode<int> head = new BinNode<int>(input);
            while (input != -999)
            {
                input = int.Parse(Console.ReadLine());
                head.SetLeft(new BinNode<int>(null, input, head));
                head = head.GetLeft();
            }
            return head;
        }


        public static void InsertList<T>(BinNode<T> ls1, BinNode<T> ls2) //o(n)
        {
            int ls1Len = Size(ls1);
            for (int i = 0; i < ls1Len/2; i++)
            {
                ls1 = ls1.GetRight();
            }
            ls1.GetLeft().SetRight(ls2);
            ls2.SetLeft(ls1.GetLeft());
            while(ls2.GetRight() != null)
            {
                ls2 = ls2.GetRight();
            }
            ls2.SetRight(ls1);
            ls1.SetLeft(ls2);

        }


        public static int Size<T>(BinNode<T> chain)
        {
            while (chain.GetLeft() != null)
            {
                chain = chain.GetLeft();
            }
            int count = 0;
            while(chain != null)
            {
                count++;
                chain = chain.GetRight();
            }
            return count;
        }
        public static int Sum(BinNode<int> chain)
        {
            while (chain.GetLeft() != null)
            {
                chain = chain.GetLeft();
            }
            int sum = 0;
            while (chain != null)
            {
                sum += chain.GetValue();
                chain = chain.GetRight();
            }
            return sum;
        }
        public static void PrintBinNode<T>(BinNode<T> lst)
        {
            while(lst.GetLeft() != null)
            {
                lst = lst.GetLeft();
            }
            while(lst != null)
            {
                Console.Write(lst + " -> ");
                lst = lst.GetRight();
            }
            Console.WriteLine();
        }
    }
}