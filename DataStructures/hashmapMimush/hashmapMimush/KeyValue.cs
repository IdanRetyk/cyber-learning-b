using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace hashmapMimush
{
    internal class KeyValue<TKey,TValue>
    {
        TKey key;
        TValue val;
        public KeyValue(TKey k , TValue v)
        {
            key = k;
            val = v;
        }

        public TKey Key
        {
            get => key;
            set => key = value;
        }

        public TValue Value
        {
            get => val;
            set => val = value;
        }
    }
}
