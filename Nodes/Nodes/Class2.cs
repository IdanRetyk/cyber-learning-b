using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading.Tasks;

namespace Nodes
{
    internal class Class1
    {
        public static bool AstricQueue(Queue<char> q)
        {
            if (q == null) return false;
            if (q.IsEmpty()) return true;

            if (q.Head() == '*')
            {
                char ch1 = q.Remove();
                if (q.IsEmpty())
                {
                    q.Insert(ch1);
                    return true;
                }
                else
                {
                    q.Insert(ch1);
                    return false;
                }
            }


            Queue<char> q1 = new Queue<char>();

            while (!q.IsEmpty())
            {
                q1.Insert(q.Remove());
            }

            Queue<char> check = new Queue<char>();

            bool returnMe = true;

            char ch;
            char prevCh = q1.Remove();
            check.Insert(prevCh);
            q.Insert(check.Head());
            bool ast = false;
            

            while (!q1.IsEmpty())
            {
                ch = q1.Remove();
                q.Insert(ch);
                if (ch == '*') ast = true;

                else if(ast)
                {
                    if (check.IsEmpty()) returnMe = false;
                    else if (ch != check.Remove()) returnMe = false;
                }

                else
                {
                    if (prevCh != ch)
                    {
                        prevCh = ch;
                        check.Insert(ch);
                    }

                }

            }

            if (!check.IsEmpty()) returnMe = false;

            return returnMe;

        }
    }
}
