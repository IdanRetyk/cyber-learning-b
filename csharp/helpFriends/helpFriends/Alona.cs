using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace helpFriends
{
    internal class Alona
    {
        public static void PrintLongestStreak(int[] arr) //longest 0's streak and indexes
        {
            int count = 0;
            int max = 0;

            int startIndex = 0;
            int maxStartIndex = 0;

            int maxEndIndex = 0;

            bool streak = false; //this repreasent if we're currently on streak
            for (int i = 0; i < arr.Length; i++)
            {


                if (arr[i] == 0 && !streak) //staring the streak
                {
                    startIndex = i;
                    count = 1;
                    streak = true;
                }
                else if (arr[i] == 0 && streak)
                {
                    count++;
                }
                else
                {
                    streak = false;
                    count = 0;
                }

                if (count > max)
                {
                    max = count;
                    maxStartIndex = startIndex;
                    maxEndIndex = startIndex + count - 1;
                }


            }
            Console.WriteLine($"largest streak is {max}, start at arr[{maxStartIndex}] and end at arr[{maxEndIndex}]");
        }
    }
}
