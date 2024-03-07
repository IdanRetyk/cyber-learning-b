using System;
using System.Collections.Generic;
using System.ComponentModel.Design;
using System.Data;
using System.Data.SqlTypes;
using System.Diagnostics.Eventing.Reader;
using System.Linq;
using System.Runtime.InteropServices;
using System.Runtime.Remoting.Messaging;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace Nodes
{
    internal class Program
    {
        public static Node<T> ToRounded<T>(Node<T> head)
        {
            Node<T> pos = head;
            while (pos.GetNext() != null)
            {
                pos = pos.GetNext();
            }
            //pos is the last elemnt
            pos.SetNext(head);
            return head;
        }

        public static void PrintRounded<T>(Node<T> head)
        {
            Console.Write(head + " -> ");
            Node<T> pos = head.GetNext();
            while(pos != head)
            {
                Console.Write(pos + " -> ");
                pos = pos.GetNext();
            }
            Console.WriteLine();
        }

        public static void UnRound<T>(Node<T> head)
        {
            Node<T> pos = head.GetNext();
            while (pos.GetNext() != head)
            {
                pos = pos.GetNext();
            }
            pos.SetNext(null);
        }


        public static bool IsRound<T>(Node<T> head)
        {
            Node<T> pos = head.GetNext();
            while(pos != null)
            {

                if (pos == head) return true;
                pos = pos.GetNext();
            }
            return false;
        }

        public static int ListCount<T>(Node<T> head)
        {
            Node<T> pos = head.GetNext();
            int i = 1;
            while(pos != head)
            {
                i++;
                pos = pos.GetNext();
            }
            return i;
        }


        public static int ListSum(Node<int> head)
        {
            Node<int> pos = head.GetNext();
            int sum = head.GetValue();
            while (pos != head)
            {
                sum += pos.GetValue();
                pos = pos.GetNext();
            }
            return sum;
        }


        public static void RemoveNode<T>(Node<T> head, int index)
        {
            for (int i = 0; i + 1< index; i++)
            {
                head = head.GetNext();
            }
            head.SetNext(head.GetNext().GetNext());
        }

        public static void RemoveFirst<T>(Node<T> head)
        {
            head.SetValue(head.GetNext().GetValue());
            RemoveNode(head, 1);
        }

        public static void RemoveLast<T>(Node<T> head)
        {
            Node<T> pos = head.GetNext();
            while(pos.GetNext().GetNext() != head)
            {
                pos = pos.GetNext();
            }
            pos.SetNext(head);
        }

        public static bool IsExist<T>(Node<T> head, T value)
        {
            if (head.GetValue().Equals(value)) return true;
            Node<T> pos = head.GetNext();
            while(pos != head)
            {
                if (pos.GetValue().Equals(value)) return true;
                pos = pos.GetNext();
            }
            return false;
        }

        public static void RemoveEvenValues(Node<int> head)
        {
            Node<int> pos = head;
            int index = 1;
            while (pos.GetNext() != head)
            {
                if (pos.GetNext().GetValue() % 2 == 0)
                    RemoveNode(head, index);
                else
                {
                    pos = pos.GetNext();
                    index++;
                }
               
            }
            if (head.GetValue() % 2 == 0)
                RemoveFirst(head);
        }

        public static void AddBeforeEvenValues(Node<int> head)
        {
            Node<int> pos = head;
            while (pos.GetNext() != head)
            {
                if (pos.GetNext().GetValue() % 2 == 0)
                {
                    //add new node
                    pos.SetNext(new Node<int>(pos.GetNext().GetValue() - 1, pos.GetNext()));
                    pos = pos.GetNext();
                }
                pos = pos.GetNext();
            }
            if (head.GetValue() % 2 == 0)
            {
                head.SetNext(new Node<int>(head.GetValue(), head.GetNext()));
                head.SetValue(head.GetValue() - 1);
                
            }

        }

        public static void AddNode<T>(Node<T> head ,T value, int index) //doesn't work for index = 0
        {
            Node<T> pos = head;
            int i = 1;
            while (pos.GetNext() != head)
            {
                if (i == index)
                {
                    pos.SetNext(new Node<T>(value, pos.GetNext()));
                }
                i++;
                pos = pos.GetNext();
            }
            if (i == index)
            {
                pos.SetNext(new Node<T>(value, pos.GetNext()));
            }
        }

        public static Node<T> AddFirst<T>(Node<T> head, T value)
        {
            head.SetNext(new Node<T>(head.GetValue(), head.GetNext()));
            head.SetValue(value);
            return head;
        }



        public static void Ex13(Node<int> head)
        {
            Node<int> pos = head;
            int index = 1;
            while (pos.GetNext() != head)
            {
                AddNode(head, pos.GetValue() + pos.GetNext().GetValue(), index);
                index += 2;
                pos = pos.GetNext().GetNext();
            }
            //pos.GetNext = head
            AddNode(head, pos.GetValue() + pos.GetNext().GetValue(),ListCount(head));
        }



        /// -+====================+-
        ///      fork list
        ///
        /// -+====================+-
        



        public static void CreateForkList<T>(Node<T> mainHead, Node<T> sideHead, int n)
        {
            while (sideHead.GetNext() != null)
            {
                sideHead = sideHead.GetNext();
            }
            //sidehead = last elemnt second list


            for (int i = 0; i < n; i++)
            {
                mainHead = mainHead.GetNext();
            }
            //mainhead = nth element
            sideHead.SetNext(mainHead);
        }


        public static Node<T> GetForkNode<T>(Node<T> head1,Node<T> head2)
        {
            while (head1 != null)
            {
                if (NodeUtils.DoesContain(head2, head1))
                    return head1;
                head1 = head1.GetNext();
            }
            return null;
        }

        public static void PasteShortestToTheEnd<T>(Node<T> head1, Node<T> head2)
        {
            Node<T> ShortList;
            Node<T> LongList;
            if (NodeUtils.CountList(head1) > NodeUtils.CountList(head2))
            {
                ShortList = head2;
                LongList = head1;
            }
            else
            {
                ShortList = head1;
                LongList = head2;
            }

            while(LongList.GetNext() != null)
            {
                LongList = LongList.GetNext();
            }

            //last element of longlist
            LongList.SetNext(ShortList);

            Node<T> CommonNode = GetForkNode(head1, head2);

            while(ShortList.GetNext() != CommonNode)
            {
                ShortList = ShortList.GetNext();
            }
            ShortList.SetNext(null);
        }




        /// -+====================+-
        ///      2/4/2024 hw 
        ///      bagurt queue
        ///
        /// -+====================+-




        public static bool IsIdentical<T>(Queue<T> q1, Queue<T> q2)
        {
            if (QueueUtils.GetSize(q1) != QueueUtils.GetSize(q2))
                return false;

            Queue<T> new1 = QueueUtils.Clone(q1);
            Queue<T> new2 = QueueUtils.Clone(q2);


            while (!new1.IsEmpty())
            {
                if (!new1.Remove().Equals(new2.Remove()))
                    return false;
            }
            return true;
        }






        public static int BigNumber(Node<Queue<int>> lst)
        {
            int max = int.MinValue;
            while (lst != null)
            {
                max = Math.Max(max, QueueUtils.ToNumber(lst.GetValue()));
            }
            return max;
        }


        



        



        static void Main(string[] args)
        {
            char[] arr1 = {  '*','5' };
            int[] arr2 = { 1, 2, 4, 1 };

            Queue<char> Q1 = QueueUtils.CreateQueueFromArray(arr1);
            Queue<int> Q2 = QueueUtils.CreateQueueFromArray(arr2);

            Console.WriteLine(Q1);

            Console.WriteLine(Class1.AstricQueue(Q1));
            Console.WriteLine(Q2);


            Console.ReadKey();


        }

       
    }
}
