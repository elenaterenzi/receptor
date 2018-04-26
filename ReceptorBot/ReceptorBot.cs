using Microsoft.Bot;
using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Microsoft.ProjectOxford.Vision;
using Microsoft.ProjectOxford.Vision.Contract;
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
                    await context.SendActivity(res);
                    /*
                    HandwritingRecognitionOperationResult res;
                    do
                    {
                        await Task.Delay(500);
                        res = await cli.GetHandwritingRecognitionOperationResultAsync(t);
                    } while (res.Status == HandwritingRecognitionOperationStatus.Running);
                    foreach(var x in res.RecognitionResult.Lines)
                    {
                        await context.SendActivity(x.Words.Fold("",(w,s) => s+" "+w.Text));
                    }
                    */
                }
                else
                {
                    await context.SendActivity("Please attach a photo of a receipt");
                }
            }
        }
    }
}
