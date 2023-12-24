using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace binaryNumbers
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Bnum num = new Bnum();


            int count = 0;
            for (int i = 0; i < 365; i++)
            {
                count += num.Count1();
                num.Add();
            }
            Console.WriteLine(count);

            Console.ReadLine();
        }
    }
}
