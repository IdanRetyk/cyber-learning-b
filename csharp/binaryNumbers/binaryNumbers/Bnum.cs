using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace binaryNumbers
{
    internal class Bnum
    {
        private int num;
        private int decimalNum;

        public static int DeciamlToBinary(int decimalNumber)
        {
            

            int remainder;
            string result = string.Empty;
            while (decimalNumber > 0)
            {
                remainder = decimalNumber % 2;
                decimalNumber /= 2;
                result = remainder.ToString() + result;
            }
            return int.Parse(result);
        }

        public Bnum(int initialValue = 1)
        {
            decimalNum = initialValue;
            num = DeciamlToBinary(initialValue);
        }

        public int GetDecimalValue()
        {
            return decimalNum;
        }

        public int GetBinaryValue()
        {
            return num;
        }

        public void Add(int amount = 1)
        {
            decimalNum++;
            num = DeciamlToBinary(decimalNum);
        }

        public int Count1()
        {
            int amountOf1 = 0;
            string stNum = num.ToString();
            for (int i = 0; i < stNum.Length; i++)
            {
                if (stNum[i] == '1')
                    amountOf1++;
            }
            return amountOf1;
        }
    }
}
