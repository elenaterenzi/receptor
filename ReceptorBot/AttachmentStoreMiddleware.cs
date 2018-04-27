using Microsoft.Bot.Builder;
using Microsoft.Bot.Schema;
using Microsoft.WindowsAzure.Storage;
using Microsoft.WindowsAzure.Storage.Auth;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace ReceptorBot
{
    public class AttachmentStoreMiddleware : IMiddleware
    {
        public string StorageAccountKey { get; set; }
        public string StorageAccountName { get; set; }
        public string StorageAccountContainer { get; set; }
        public bool ReplaceUri { get; set; }
        public bool AppendGuid { get; set; } = true;
        public AttachmentStoreMiddleware(string Acct, string Key, string Dir, bool ReplaceUri = false)
        {
            StorageAccountKey = Key;
            StorageAccountName = Acct;
            StorageAccountContainer = Dir;
            this.ReplaceUri = ReplaceUri;
        }

        public async Task OnTurn(ITurnContext context, MiddlewareSet.NextDelegate next)
        {
            if (context.Activity.Type == ActivityTypes.Message
                && context.Activity.Attachments?.Count>0)
            {
                var http = new HttpClient();
                var sa = new CloudStorageAccount(new StorageCredentials(StorageAccountName, StorageAccountKey),true);
                var ccli = sa.CreateCloudBlobClient();
                var ctr = ccli.GetContainerReference(StorageAccountContainer);
                await ctr.CreateIfNotExistsAsync();
                foreach (var x in context.Activity.Attachments)
                {
                    var str = await http.GetStreamAsync(x.ContentUrl);
                    var f = ctr.GetBlockBlobReference(AppendGuid ? $"{Guid.NewGuid()}_{x.Name}" : x.Name);
                    await f.UploadFromStreamAsync(str);
                    if (ReplaceUri) x.ContentUrl = f.StorageUri.PrimaryUri.AbsoluteUri;
                }
            }
            await next();
        }
    }
}
