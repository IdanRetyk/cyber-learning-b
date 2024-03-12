using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading.Tasks;

namespace Nodes
{
    internal class Class1
    {
        public bool AstricQueue(Queue<char> q)
        {
            if (q == null) return false;
            if (q.IsEmpty()) return true;

            if (q.Head() == '*')
            {
                char ch = q.Remove();
                if (q.IsEmpty())
                {
                    q.Insert(ch);
                    return true;
                }
                else
                {
                    q.Insert(ch);
                    return false;
                }
            }


            Queue<char> q1 = new Queue<char> ();
            while (!q.IsEmpty())
            {
                q1.Insert(q.Remove());
            }
            Queue<char> check = new Queue<char> ();

            bool returnMe = true;

            char ch;
            check.Insert(q1.Remove());
            q.Insert(check.Head());
            bool ast = false;
            char prevCh;

            while (!q1.IsEmpty())
            {
                ch = q1.()
            }
        } 
    }
}
