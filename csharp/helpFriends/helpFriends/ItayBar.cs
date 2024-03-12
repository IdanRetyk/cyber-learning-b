using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace helpFriends
{
    internal class ItayBar
    {
        int num = 10;
        int[] arr = new int[5];
        public static void PrintInt(int num)
        {

        }
        public static void PrintArr(int[] arr)
        {
            Console.Write("[");
            for (int i = 0; i < arr.Length; i++)
            {

                Console.Write(arr[i] + ",");
            }
            Console.Write("]");
        }

        public static int[] SwitchPair(int[] arr)
        {
            int[] newArr = new int[arr.Length]; //building the array we will return

            for (int i = 0; i < arr.Length - 1; i += 2)
            {
                newArr[i + 1] = arr[i];
                newArr[i] = arr[i + 1];
            }

            return newArr;
        }
    }
}
