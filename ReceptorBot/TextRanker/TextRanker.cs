using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ReceptorBot.TextRanker
{
    public class Ranker<T>
    {
        public Func<T,int> Metric { get; set; }
        public Ranker(Func<T,int> metric)
        {
            this.Metric = metric;
        }

        public T Top(IEnumerable<T> seq)
        {
            return seq.OrderBy(Metric).First();
        }
    }

    public static class TextMetrics
    {
        public static int Count(Func<char,bool> f, string s)
        {
            int n = 0;
            foreach (var x in s.ToCharArray())
                if (f(x)) n++;
            return n;
        }
        public static int Count(char[] set, string s) => Count((x) => set.Contains(x),s);

        public static int NCount(char[] set, string s) => Count((x) => !set.Contains(x), s);

        public static int Digits(string s) => Count(new char[] { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' }, s);

        public static int Date(string s)
        {
            var n = Digits(s);
            var m = s.Length - n;
            if (s.Contains('l') || s.Contains('|')) m = m - 2;
            if (s.Contains('/') || s.Contains('.')) m = m - 4;
            int z = 0;
            if (n < 6) z = (6 - n)*3;
            if (n > 8) z = (n - 8) * 3;
            z = z + m;
            return z;
        }

        public static int Amount(string s)
        {
            var n = Digits(s);
            var m = s.Length - n;
            int z = 0;
            if (n < 2) z = (2 - n) * 3;
            if (n > 5) z = (n - 5) * 3;
            z = z + m;
            return z;
        }
    }

    public class TextUtils
    {
        public static string DigiTrim(string s)
        {
            while (s.Length > 0 && !Char.IsDigit(s[0])) s = s.Substring(1);
            while (s.Length > 0 && !Char.IsDigit(s[s.Length-1])) s = s.Substring(0,s.Length-1);
            return s;
        }
        
        public static string Unspacify(string s)
        {
            int n;
            while((n = s.IndexOf(' '))>=0)
            {
                s = s.Remove(n, 1);
            }
            return s;
        }
    }

}
