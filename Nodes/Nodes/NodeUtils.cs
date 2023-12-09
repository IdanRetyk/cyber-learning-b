using Nodes;
using System;
using System.Reflection;

namespace Nodes
{
    internal class NodeUtils
    {
        public static Node<T> CreateListFromArray<T>(T[] arr)
        {
            Node<T> head = new Node<T>(arr[0]);
            Node<T> prevNode = head;
            for (int i = 1; i < arr.Length; i++)
            {
                Node<T> currNode = new Node<T>(arr[i]);
                prevNode.SetNext(currNode);
                prevNode = currNode;
            }
            return head;
        }

        public static Node<T> CreateListFromArrayR<T>(T[] arr, int index)
        {
            if (index == arr.Length - 1)
            {
                return new Node<T>(arr[index]);
            }
            if (arr.Length == 0)
            {
                return null;
            }
            return new Node<T>(arr[index], CreateListFromArrayR<T>(arr, index + 1));
        }

        public static void PrintList<T>(Node<T> head)
        {
            while (head != null)
            {
                Console.Write(head + ", ");
                head = head.GetNext();
            }
            Console.WriteLine();
        }

        public static void PrintListR<T>(Node<T> head)
        {
            if (head != null)
            {
                Console.WriteLine(head);
                PrintListR(head.GetNext());
            }
        }

        public static bool CompareList<T>(Node<T> head1, Node<T> head2)
        {
            bool returnMe = true;
            while (head1 != null && head2 != null)
            {
                if (!head1.GetValue().Equals(head2.GetValue()))
                {
                    returnMe = false;
                }
                head1 = head1.GetNext();
                head2 = head2.GetNext();
            }
            if (head2 != null || head1 != null) //only one of the lists ended -> not equal
            {
                returnMe = false;
            }

            return returnMe;
        }

        public static bool CompareListR<T>(Node<T> head1, Node<T> head2)
        {
            if (head1 == null ^ head2 == null) //if one list ended but not both of them
                return false;
            if (head1 != null && head2 != null)
                return CompareListR(head1.GetNext(), head2.GetNext()) && head1.GetValue().Equals(head2.GetValue());
            return true;
        }

        public static int CountList<T>(Node<T> head)
        {
            int count = 0;
            while (head != null)
            {
                head = head.GetNext();
                count++;
            }
            return count;
        }

        public static int CountListR<T>(Node<T> head)
        {
            if (head == null)
            {
                return 0;
            }
            return CountListR(head.GetNext()) + 1;
        }

        public static int SumList(Node<int> head)
        {
            int sum = 0;
            while (head != null)
            {
                sum += head.GetValue();
                head = head.GetNext();
            }
            return sum;
        }

        public static int SumListR(Node<int> head)
        {
            if (head == null)
            {
                return 0;
            }
            return SumListR(head.GetNext()) + head.GetValue();
        }

        public static bool IsExist<T>(Node<T> head, T value)
        {
            bool returnMe = false;
            while (head != null)
            {
                if (head.GetValue().Equals(value))
                    returnMe = true;
                head = head.GetNext();
            }
            return returnMe;
        }

        public static bool DoesContain<T>(Node<T> head, Node<T> element)
        {
            if (head == null)
                return false;
            return head == element || DoesContain(head.GetNext(), element);
        }

        public static bool IsExistR<T>(Node<T> head, T value)
        {
            if (head == null)
                return false;
            return head.GetValue().Equals(value) || IsExistR(head.GetNext(), value);
        }

        public static int ListMax(Node<int> head)
        {
            int max = int.MinValue;
            while (head != null)
            {
                max = Math.Max(max, head.GetValue());
                head = head.GetNext();
            }
            return max;
        }

        public static int ListMaxR(Node<int> head)
        {
            if (head == null)
                return int.MinValue;
            return Math.Max(ListMaxR(head.GetNext()), head.GetValue());
        }

        public static void ListPositive(Node<int> head)
        {
            while (head != null)
            {
                head.SetValue(Math.Abs(head.GetValue()));
                head = head.GetNext();
            }
        }

        public static void ListPositiveR(Node<int> head)
        {
            if (head != null)
            {
                head.SetValue(Math.Abs(head.GetValue()));
                ListPositiveR(head.GetNext());
            }
        }

        public static Node<T> GetElement<T>(Node<T> head, T value)
        {
            while (head != null)
            {
                if (head.GetValue().Equals(value))
                    return head;
                head = head.GetNext();
            }
            return null;
        }

        public static Node<T> GetElementR<T>(Node<T> head, int n)
        {
            if (head == null)//list is shorter than n
                return null;
            if (n == 1)
                return head;
            return GetElementR(head.GetNext(), n - 1);
        }


        public static bool IsSorted(Node<int> head)
        {
            bool isSorted = true;
            while (head.GetNext() != null && isSorted)
            {
                if (head.GetValue() > head.GetNext().GetValue())
                    isSorted = false;
                head = head.GetNext();
            }
            return isSorted;

        }


        public static int StreakCount(Node<int> head, int num)
        {
            int streakCount = 0;
            bool currentlyOnStreak = false;
            while (head != null)
            {
                if (head.GetValue() == num && !currentlyOnStreak) //starting a streak
                {
                    currentlyOnStreak = true;
                    streakCount++;
                }
                if (currentlyOnStreak && head.GetValue() != num) //break the streak
                {
                    currentlyOnStreak = false;
                }
                head = head.GetNext();
            }
            return streakCount;
        }

        public static void PrintSubList<T>(Node<T> head, int i, int j)
        {
            int index = 0;
            while (head != null)
            {
                if (index > i && index < j)
                {
                    Console.Write(head.GetValue() + ", ");
                }
                head = head.GetNext();
                index++;
            }
        }

        public static Node<T> RemoveDoubles<T>(Node<T> head)
        {
            Node<T> returnMe = new Node<T>(head.GetValue());
            Node<T> newHead = returnMe;
            while (head != null)
            {
                if (!IsExist(newHead, head.GetValue())) //if element doesnt already exist
                {
                    newHead.SetNext(new Node<T>(head.GetValue()));
                    newHead = newHead.GetNext();
                }
                head = head.GetNext();

            }
            return returnMe;
        }

        public static bool IsStable(Node<int> head)
        {
            double average = (double)SumList(head) / CountList(head);
            int above = 0;
            int below = 0;
            while (head != null)
            {
                if (head.GetValue() < average)
                    below++;
                if (head.GetValue() > average)
                    above++;
                head = head.GetNext();
            }
            return below == above;

        }


        public static Node<int> IsolateBiggestElement(Node<int> head)
        {
            if (head.GetNext() == null)//list is one element
            {
                return head;
            }


            int index = 0;
            int max = int.MinValue;
            int maxIndex = 0;
            Node<int> backupHead = head;
            while (backupHead != null)
            {
                if (max < backupHead.GetValue())
                {
                    max = backupHead.GetValue();
                    maxIndex = index;
                }
                backupHead = backupHead.GetNext();
                index++;
            }

            if (maxIndex == 0)
            {
                //this part saves the node you need to return before you move forward
                Node<int> returnMe = new Node<int>(head.GetValue());
                //this part 'removes' first node (it actually moves the second node to the first node and than remove second node
                head.SetValue(head.GetNext().GetValue()); //shifting second node value to first node
                head.SetNext(head.GetNext().GetNext()); //connecting first node to third node
                return returnMe;
            }


            index = 0;
            while (head != null && index != maxIndex)
            {
                if (index + 1 == maxIndex)
                {
                    Node<int> returnMe = head.GetNext();
                    head.SetNext(head.GetNext().GetNext()); //connect previous element to next element
                    returnMe.SetNext(null);
                    return returnMe;
                }
                head = head.GetNext();
                index++;
            }
            return null;
        }


        public static void InsertToSortedList(Node<int> head, Node<int> node)
        {
            bool nodeInserted = false;
            while (head.GetNext() != null && !nodeInserted)
            {
                if (head.GetNext().GetValue() > node.GetValue())
                {
                    node.SetNext(head.GetNext());
                    head.SetNext(node);
                    nodeInserted = true;
                }
                head = head.GetNext();
            }
            if (!nodeInserted) //new node is bigger than the biggest item on the list
                head.SetNext(node);
        }


        public static Node<int> SortList(Node<int> head)
        {
            Node<int> newList = IsolateBiggestElement(head);
            Node<int> sortedHead = newList;
            while (head.GetNext() != null) //this will only happen if there is one emelent left
            {
                newList.SetNext(IsolateBiggestElement(head));
                newList = newList.GetNext();
            }
            newList.SetNext(head);
            return ReverseList(sortedHead);

        }

        public static Node<T> ReverseList<T>(Node<T> head)
        {
            Node<T> prev = null, curr = head, next = head.GetNext();
            while (curr != null)
            {
                curr.SetNext(prev);
                prev = curr;
                curr = next;
                if (next != null)
                    next = next.GetNext();
            }
            return prev;
        }


        public static int LongestNegativeStreak(Node<int> head)
        {
            int longestStreak = 0;
            int currentStreak = 0;
            bool currentlyOnStreak = false;
            while (head != null)
            {
                if (head.GetValue() < 0)
                {
                    currentlyOnStreak = true;
                    currentStreak++;
                }
                else if (head.GetValue() > 0 && currentlyOnStreak)
                {
                    currentlyOnStreak = false;

                    currentStreak = 0;

                }
                longestStreak = Math.Max(longestStreak, currentStreak);
                head = head.GetNext();
            }
            return longestStreak;
        }


        public static Node<int> MergeLists(Node<int> head1, Node<int> head2)
        {
            Node<int> newHead;
            if (head1.GetValue() > head2.GetValue())
            {
                newHead = new Node<int>(head2.GetValue());
                head2 = head2.GetNext();
            }
            else
            {
                newHead = new Node<int>(head1.GetValue());
                head1 = head1.GetNext();
            }
            Node<int> returnMe = newHead;
            while (head1 != null && head2 != null)
            {
                if (head1.GetValue() > head2.GetValue())
                {
                    newHead.SetNext(new Node<int>(head2.GetValue()));
                    newHead = newHead.GetNext();
                    head2 = head2.GetNext();
                }
                else
                {
                    newHead.SetNext(new Node<int>(head1.GetValue()));
                    newHead = newHead.GetNext();
                    head1 = head1.GetNext();
                }
            }
            while (head1 != null)
            {
                newHead.SetNext(new Node<int>(head1.GetValue()));
                newHead = newHead.GetNext();
                head1 = head1.GetNext();
            }
            while (head2 != null)
            {
                newHead.SetNext(new Node<int>(head2.GetValue()));
                newHead = newHead.GetNext();
                head2 = head2.GetNext();
            }
            return returnMe;
        }

        public static void InsertNode(Node<int> head, int value)
        {
            bool cont = true;
            while (head != null && cont)
            {
                if (head.GetValue() == value)
                {
                    Node<int> newNode = new Node<int>(value + 1, head.GetNext());
                    head.SetNext(newNode);
                    cont = false;
                }
                head = head.GetNext();
            }
        }

        public static Node<T> CutLists<T>(Node<T> head1, Node<T> head2)
        {
            Node<T> newList = null;

            while (newList == null && head1 != null) //until we have found atleast one elemetnt
            {
                if (IsExist(head2, head1.GetValue()))
                {
                    newList = new Node<T>(head1.GetValue());
                }
                head1 = head1.GetNext();
            }
            Node<T> returnMe = newList;
            while (head1 != null)
            {
                if (IsExist(head2, head1.GetValue()))
                {
                    newList.SetNext(new Node<T>(head1.GetValue()));
                    newList = newList.GetNext();
                }
                head1 = head1.GetNext();
            }
            return returnMe;
        }

        public static void AddNode<T>(Node<T> head, T value, int index)
        {
            int i = 1;
            while (head.GetNext() != null)
            {
                if (i == index)
                {
                    head.SetNext(new Node<T>(value, head.GetNext()));
                }
                i++;
                head = head.GetNext();
            }
            if (i == index)
            {
                head.SetNext(new Node<T>(value, head.GetNext()));
            }
        }
    }
}
