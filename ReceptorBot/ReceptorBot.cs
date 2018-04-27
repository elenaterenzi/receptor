using Microsoft.Bot;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Newtonsoft.Json;
using ReceptorBot.TextRanker;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace ReceptorBot
{
    public class ReceptorBot : IBot
    {
        public async Task OnTurn(ITurnContext context)
        {
            if (context.Activity.Type == ActivityTypes.Message)
            {
                var msg = context.Activity;
                if (msg.Attachments?.Count > 0)
                {
                    var http = new HttpClient();
                    var str = await http.GetStreamAsync(msg.Attachments[0].ContentUrl);
                    var cli = new OcrClient(Config.VisionApiKey, "https://westus.api.cognitive.microsoft.com/vision/v1.0/");
                    var res = await cli.StartOcrAsync(str);
                    res = await cli.GetOcrResult(res);
                    // await context.SendActivity(res);
                    dynamic js = JsonConvert.DeserializeObject(res);
                    var lines = new List<string>();
                    foreach (dynamic x in js.recognitionResult.lines)
                    {
                        lines.Add(x.text.ToString());
                    }
                    await context.SendActivity(lines.Aggregate((a, b) => $"{a}\r\n{b}"));
                    lines = lines.Select(x => TextUtils.Unspacify(TextUtils.DigiTrim(x))).Where(x => x.Length >= 2).ToList();
                    if (lines==null || lines.Count<1)
                    {
                        await context.SendActivity("Sorry, nothing suitable found");
                    }
                    else
                    {
                        var DR = new Ranker<string>(TextMetrics.Date);
                        var AR = new Ranker<string>(TextMetrics.Amount);
                        await context.SendActivity($"Date={DR.Top(lines)}, Amount={AR.Top(lines)}");
                    }
                }
                else
                {
                    await context.SendActivity("Please attach a photo of a receipt");
                }
            }
        }

    }
}
