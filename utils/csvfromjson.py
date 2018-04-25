########### Python 3.2 #############
import glob, os
import json
import pandas as pd

def js_r(filepath):
     with open(filepath, encoding='utf-8') as f_in:
         return(json.load(f_in))


image_path = "yourfolder"
image_path=os.path.realpath(image_path)


def create_jsonfiles(image_path, jsonpattern='yourpattern'):
    for f in sorted(glob.glob(os.path.join(image_path,'*'+jsonpattern+'.json'))):
        print(f)
        df = pd.DataFrame()
        analysis = js_r(f)
        text = []
        boundingBox =[]
        linestxt=[]
        linesbbox=[]
        for l in analysis["content"]["lines"]:
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
