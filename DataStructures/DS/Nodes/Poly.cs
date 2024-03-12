using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
namespace Nodes
{
    internal class Poly
    {
        
        private Node<(int, int)> head;

        public Poly(Node<(int, int)> head)
        {
            this.head = head;
        }

        public Node<(int, int)> GetHead()
        {
            return head;
        }


        public Poly SortPoly(Poly poly) 
        {
            Node<(int,int)> newList = IsolateBiggestElement(poly.GetHead());
            Node<(int,int)> sortedHead = newList;
            while (head.GetNext() != null) //this will only happen if there is one emelent left
            {
                newList.SetNext(IsolateBiggestElement(head));
                newList = newList.GetNext();
            }
            newList.SetNext(head);
            return new Poly(sortedHead);


        }

        public void MergeElements()
        {
            Node<(int, int)> lst = head;
            while (lst != null)
            {
                Node<(int, int)> i = lst;
                while (i.GetNext() != null)
                {
                    if (i.GetNext().GetValue().Item2 == lst.GetValue().Item2)
                    {
                        lst.SetValue((i.GetNext().GetValue().Item1 + lst.GetValue().Item1, lst.GetValue().Item2));

                        //remove i.getnext
                        i.SetNext(i.GetNext().GetNext());
                        

                    }
                    i = i.GetNext();
                }
                lst = lst.GetNext();
            }
        }

        public double Calc(int x)
        {
            double result = 0;
            Node<(int, int)> list = head;

            while (list != null)
            {
                result += list.GetValue().Item1 * Math.Pow(x, list.GetValue().Item2);
            }
            return result;
        }

        public override string ToString()
        {
            string st = "";
            //first element
            if (head.GetValue().Item1 < 0)
                st += "- ";
            st += Math.Abs(head.GetValue().Item1) + "*X^" + head.GetValue().Item2;
            
            Node<(int, int)> lst = head;
            while (lst != null)
            {
                if (head.GetValue().Item1 > 0)
                    st += "+ ";
                st += head.GetValue().Item1 + "*X^" + head.GetValue().Item2;
            }
            return st;
        }

        public static Node<(int,int)> IsolateBiggestElement(Node<(int,int)> head)
        {
            if (head.GetNext() == null)//list is one element
            {
                return head;
            }


            int index = 0;
            int max = int.MinValue;
            int maxIndex = 0;
            Node<(int,int)> backupHead = head;
            while (backupHead != null)
            {
                if (max < backupHead.GetValue().Item2)
                {
                    max = backupHead.GetValue().Item2;
                    maxIndex = index;
                }
                backupHead = backupHead.GetNext();
                index++;
            }

            if (maxIndex == 0)
            {
                //this part saves the node you need to return before you move forward
                Node<(int,int)> returnMe = new Node<(int,int)>(head.GetValue());
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
                    Node<(int,int)> returnMe = head.GetNext();
                    head.SetNext(head.GetNext().GetNext()); //connect previous element to next element
                    returnMe.SetNext(null);
                    return returnMe;
                }
                head = head.GetNext();
                index++;
            }
            return null;
        }


    }
}
