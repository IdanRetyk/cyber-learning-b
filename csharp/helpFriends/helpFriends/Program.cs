using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace helpFriends
{
    internal class Program
    {
        static void Main(string[] args)
        {
            int[] arr = {1,2,3,4,5,6};
            //Alona.PrintLongestStreak(arr);

            int[] switchArr = ItayBar.SwitchPair(arr);

            PrintArr(switchArr);



            Console.ReadKey();
        }

        public static void PrintArr(int[] arr)
        {
            Console.Write("[");
            for (int i = 0; i < arr.Length; i++)
            {
                Console.Write(arr[i]+ ", ");
            }
            Console.Write("]"); 
        }
    }
}
