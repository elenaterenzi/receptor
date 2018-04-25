using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ReceptorBot
{
    public static class Utils
    {
        public static U Fold<T,U>(this IEnumerable<T> seq, U i, Func<T,U,U> f)
        {
            foreach(var x in seq)
            {
                i = f(x, i);
            }
            return i;
        }
    }
}
