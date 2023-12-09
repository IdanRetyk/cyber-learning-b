using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Nodes
{
    internal class Node<T>
    {
        private T value;
        private Node<T> next;


        public Node(T value)
        {
            this.value = value;
            this.next = null;
        }

        public Node(T value, Node<T> next) 
        {
            this.next = next;
            this.value = value;
        }

        public T GetValue()
        {
            return this.value;
        }

        public Node<T> GetNext()
        {
            return this.next;
        }

        public void SetValue(T value)
        {
            this.value = value;
        }

        public void SetNext(Node<T> next)
        {
            this.next = next;
        }

        public bool HasNext()
        {
            return this.next != null;
        }

        public override string ToString()
        {
            return this.value.ToString();
        }
    }
}
