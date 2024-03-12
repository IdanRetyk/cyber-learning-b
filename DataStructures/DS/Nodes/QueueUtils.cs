using System;
using System.Runtime.InteropServices;

namespace Nodes
{
    class QueueUtils
    {
        public static Queue<T> CreateQueueFromArray<T>(T[] arr)
        {
            Queue<T> s = new Queue<T>();
            for (int i = 0; i < arr.Length; i++)
            {
                s.Insert(arr[i]);
            }
            return s;
        }
        public static void SpilledOn<T>(Queue<T> dest, Queue<T> src)
        {
            while (!src.IsEmpty())
            {
                dest.Insert(src.Remove());
            }
        }

        public static Queue<T> Clone<T>(Queue<T> s)
        {
            Queue<T> tmp = new Queue<T>();
            Queue<T> s2 = new Queue<T>();

            SpilledOn(tmp,s);
            while (!tmp.IsEmpty())
            {
                T temp = tmp.Remove();
                s.Insert(temp);
                s2.Insert(temp);
            }

            return s2;
        }
        public static int GetSize<T>(Queue<T> q)
        {
            int count = 0;
            Queue<T> backup = Clone(q);
            while (!backup.IsEmpty())
            {
                backup.Remove();
                count++;
            }
            q = backup;
            return count;
        }
        public static int Sum(Queue<int> q)
        {
            int sum = 0;
            Queue<int> backup = Clone(q);
            while (!backup.IsEmpty())
            {
                sum+= backup.Remove(); 
            }
            return sum;

        }
        public static bool IsExist<T>(Queue<T> q, T e)
        {
            bool IsExist = false;
            Queue<T> backup = Clone(q);
            while (!backup.IsEmpty() && !IsExist)
            {
                if (backup.Remove().Equals(e))
                    IsExist = true;
            }
            return IsExist;
        }
        public static void Sort(Queue<int> q)
        {
            Queue<int> q2 = new Queue<int>();
            int len = GetSize(q);
            SpilledOn(q2, q); //q is now epmty
            for (int i = 0; i < len; i++)
            {
                q.Insert(RemoveMin(q2));
            }
        }

        public static int RemoveMin(Queue<int> q1)
        {
            Queue<int> q2 = new Queue<int>();
            Queue<int> q3 = new Queue<int>();
            SpilledOn(q2, q1);
            int min = int.MaxValue;
            int num;
            //find min value. at the end q1 is still emtpy
            while (!q2.IsEmpty())
            {
                num = q2.Remove();
                if (num < min)
                {
                    min = num;
                }
                q3.Insert(num);
            }

            //restore q1 without min value
            bool found = false;
            SpilledOn(q2, q3);
            while (!q2.IsEmpty())
            {
                num = q2.Remove();
                if (num == min)
                {
                    if (found)
                        q1.Insert(num);
                    else
                        found = true;
                }
                else
                {
                    q1.Insert(num);
                }
            }

            return min;
        }





        public static Queue<T> DoubleToPalindromS<T>(Queue<T> qd)
        {
            Stack<T> myStack =new Stack<T>();
            while (!qd.IsEmpty())
            {
                qd.Remove();
                T num = qd.Remove();
                myStack.Push(num);
            }

            Stack<T> newStack = new Stack<T>();

            while (!myStack.IsEmpty())
            {
                T num = myStack.Pop();
                newStack.Push(num);
                qd.Insert(num);
            }

            while (!newStack.IsEmpty())
            {
                qd.Insert(newStack.Pop());
            }
            return qd;
        }

        public static Queue<T> DoubleToPalindromQ<T>(Queue<T> qd)
        {

            Queue<T> first = Recr(qd);
            Queue<T> last = new Queue<T>();
            SpilledOn(first, Recr(qd));
            return first;
        }

        private static Queue<T> Recr<T>(Queue<T> q)
        {
            if (q.IsEmpty())
                return null;
            Queue<T> newQ = Clone(q);
            Queue<T> final = Recr(q);
            final.Insert(newQ.Remove());
            return final;
        }



        public static int ToNumber(Queue<int> q)
        {
            int num = 0;

            num = q.Remove();
            while(!q.IsEmpty())
            {
                num *= 10;
                num += q.Remove();
            }
            return num;
        }





    }
}











