using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace HelpBar
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter num");
            
            int num = int.Parse(Console.ReadLine()); // "50"

            Console.WriteLine("num = " + num);
            //comment 


            bool var = num == 10;
            bool newVar = false;
            
            if (var)
            {
                Console.WriteLine("num is ten");
            }




            Console.ReadKey();

        }
    }
}
