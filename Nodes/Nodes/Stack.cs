using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes
{
    class Stack<T>
    {
        Node<T> lst;
        public Stack()
        {
            lst = null;
        }
        public void Push(T x)
        {
            this.lst = new Node<T>(x, lst);
        }
        public T Pop()
        {
            Node<T> prev = lst;
            lst = lst.GetNext();
            return prev.GetValue();
        }
        public T Top()
        {
            return this.lst.GetValue();
        }
        public bool IsEmpty()
        {
            return lst == null;
        }
        public override string ToString()
        {
            Node<T> node = lst;
            string s = "|";
            for (; node != null; node = node.GetNext())
            {
                s += node.GetValue().ToString();
                if (node.GetNext() != null)
                    s += ",";
            }
            return s + "|";
        }
    }




}
