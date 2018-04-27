########### Python 3.2 #############
import urllib.parse, requests,glob, os
import time,json
from PIL import Image
import pandas as pd
from azure.storage.blob import BlockBlobService

account_key='yourkey=='
account_name='youraccount'
container='travelrefunds'
prefix='taxi_receipts'
subscription_key = "yourkey"
assert subscription_key
vision_base_url = "https://yourlocation.api.cognitive.microsoft.com/vision/v1.0/"
vision_ocr_url = vision_base_url + 'ocr'
text_recognition_url = vision_base_url + "RecognizeText"

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params   = {'handwriting' : True}

image_path = "test"
image_path=os.path.realpath(image_path)


def js_r(filepath):
    with open(filepath, encoding='utf-8') as f_in:
        return(json.load(f_in))

def create_csvfromjson(image_path, jsonpattern='yourpattern', startnode="recognitionResult"): #or startnode="content"
    for f in sorted(glob.glob(os.path.join(image_path,'*'+jsonpattern+'.json'))):
        print(f)
        df = pd.DataFrame()
        analysis = js_r(f)
        text = []
        boundingBox =[]
        linestxt=[]
        linesbbox=[]
        for l in analysis[startnode]["lines"]:
            for w in l["words"]:
                linestxt.append(l["text"])
                linesbbox.append(l["boundingBox"])
                text.append(w["text"])
                boundingBox.append(w["boundingBox"])
        x1=[]
        y1=[]
        x2=[]
        y2=[]
        x3=[]
        y3=[]
        x4=[]
        y4=[]
        for b in boundingBox:
            x1.append(b[0])
            y1.append(b[1])
            x2.append(b[2])
            y2.append(b[3])
            x3.append(b[4])
            y3.append(b[5])
            x4.append(b[6])
            y4.append(b[7])
        df["linetext"]=linestxt
        df["linebbox"]=linesbbox
        df["text"]=text
        df["boundingBox"]=boundingBox
        df["x1"]=x1
        df["y1"]=y1
        df["x2"]=x2
        df["y2"]=y2
        df["x3"]=x3
        df["y3"]=y3
        df["x4"]=x4
        df["y4"]=y4
        #save to file
        df.to_csv(f.split(".")[0]+'.csv',sep=',', encoding='utf-8')

def createjsonfromfolder(image_path):
    import time
    for f in sorted(glob.glob(os.path.join(image_path,'*.jpg'))):
        print(f)
        image_data = open(f, "rb").read()
        response =''
        while response == '':
            try:
                response = requests.post(text_recognition_url , headers=headers, params=params, data=image_data)
                break
            except requests.exceptions.RequestException as e:
                print(e)
                print("Connection refused by the server... waiting 5 seconds")
                time.sleep(5)
                continue
        response.raise_for_status()
        #operation_url = response.headers["Operation-Location"]
        analysis = {}
        while not "recognitionResult" in analysis:
            response_final = requests.get(response.headers["Operation-Location"], headers=headers)
            analysis       = response_final.json()
            time.sleep(1)
        with open(f.split('.')[0]+'.json', 'w') as f_out:
            json.dump(analysis,f_out)


def list_files_in_container(blob_client,container,prefix, suffix):
    blobs = [blob.name for blob in blob_client.list_blobs(container) if prefix in blob.name and suffix in blob.name]
    return blobs

def download_blob(blob_client, container,prefix,savedir, blob):
    blob_client.get_blob_to_path(container_name=container, blob_name= blob, file_path= savedir+blob.replace(prefix,''))
    return savedir+blob.replace(prefix,'')


def upload_blob(blob_client, container, blobname, localfile):
    blob_client.create_blob_from_path(container,
                                    blobname,
                                    localfile)



if __name__ == '__main__':
    blob_client = BlockBlobService(account_name=account_name,account_key=account_key)
    blobs=list_files_in_container(blob_client, container, prefix, '.jpg')

    i=0
    for blob in blobs:
        i=i+1
        if i>61:
            print('downloading file {0} of {1}'.format(i,len(blobs)))
            jpg_file=download_blob(blob_client,container,prefix,image_path,blob)
            jpg_img=Image.open(jpg_file)
            width, height = jpg_img.size
            if width>3200 or height>3200: # max size for image is 3200x3200
                w_ratio = width/3200
                h_ratio = height/3200
                ratio= max(w_ratio,h_ratio)
                new_width = int(width*1/ratio)
                new_heigth=int(height*1/ratio)
                jpg_img=jpg_img.resize((new_width,new_heigth))
                jpg_img.save(jpg_file)
            jpg_img.close()
            print('calling API')
            createjsonfromfolder(image_path)
            print('converting to csv')
            create_csvfromjson(image_path=image_path, jsonpattern='')
            print('uploading json and csv')
            blob_name=prefix+jpg_file.replace('.jpg','.json').replace(image_path,'')
            upload_blob(blob_client,container,blob_name,jpg_file.replace('.jpg','.json'))
            blob_name=prefix+jpg_file.replace('.jpg','.csv').replace(image_path,'')
            upload_blob(blob_client,container,blob_name,jpg_file.replace('.jpg','.csv'))
            print('removing temporary files')
            os.remove(jpg_file.replace('.jpg','.json'))
            print(jpg_file.replace('.jpg','.json'))
            os.remove(jpg_file.replace('.jpg','.csv'))
            print(jpg_file.replace('.jpg','.csv'))
            os.remove(jpg_file)
            print(jpg_file)
            print('progress {} out of {}'.format(i,len(blobs)))