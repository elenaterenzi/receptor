using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Threading.Tasks;

namespace ReceptorBot
{
    public class OcrClient
    {
        public string ApiKey { get; set; }
        public string ApiEndpoint { get; set; }

        protected HttpClient _http;
        public HttpClient http
        {
            get
            {
                if (_http==null)
                {
                    _http = new HttpClient();
                    _http.DefaultRequestHeaders.Add("Ocp-Apim-Subscription-Key", ApiKey);
                }
                return _http;
            }
        }

        public OcrClient(string key, string endpoint)
        {
            ApiEndpoint = endpoint;
            ApiKey = key;
            if (!ApiEndpoint.EndsWith("/")) ApiEndpoint += "/";
        }

        public async Task<string> StartOcrAsync(Stream str)
        {
            var cont = new StreamContent(str);
            cont.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");
            var resp = await http.PostAsync($"{ApiEndpoint}recognizeText?handwriting=true", cont);
            if (resp.StatusCode == System.Net.HttpStatusCode.Accepted)
            {
                return resp.Headers.Where(x => x.Key == "Operation-Location").Select(x => x.Value).First().First();
            }
            else
            {
                throw new Exception($"Cognitive API call ended with status code={resp.StatusCode}");
            }
        }

        public async Task<string> GetOcrResult(string url, int n=3, int delay=1000)
        {
            string res;
            string st;
            do
            {
                await Task.Delay(delay);
                res = await http.GetStringAsync(url);
                dynamic t = JsonConvert.DeserializeObject(res);
                st = t.status.ToString();
            }
            while (n-->0 && st=="Running");
            return res;
        }
    }
}
