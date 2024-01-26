using Nodes;
using System.Runtime.Remoting.Messaging;

namespace Nodes
{
    public class Queue<T>
    {
        private Node<T> first;
        private Node<T> last;

        public Queue()
        {
            first = null;
            last = null;
        }

        public bool IsEmpty()
        {
            return first == null;
        }

        public void Insert(T x)
        {
            if (first == null)
            {
                first = new Node<T>(x);
                last = first;
            }
            else
            {
                last.SetNext(new Node<T>(x));
                last = last.GetNext();
            }
      
        }

        public T Remove()
        {
            T returnMe = first.GetValue();
            first = first.GetNext();
            return this.Head();
        }

        public T Head()
        {
            return this.first.GetValue();
        }

        public override string ToString()
        {
            if (first == null)
                return "queue is empty";
            string msg = "[";
            while (first != last)
            {
                msg += $"{first.GetValue()} ," ;
                first = first.GetNext();
            }
            msg += $"{first.GetValue()}]";
            return msg;
        }
    }
}
