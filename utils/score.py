import json,  pickle
import numpy as np
import os

#import label_map_util



def init():
    global detection_model
    with open('logreg_model.pkl', 'rb') as f:
        detection_model = pickle.load(f)


def create_df_from_json(jsondata,startnode="recognitionResult"):
    df = pd.DataFrame()
    analysis = jsondata
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
    return df

def run(input_df):
    try:
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:
                # Definite input and output Tensors for detection_graph
                image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
                # Each box represents a part of the image where a particular object was detected.
                detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
                # Each score represent how level of confidence for each of the objects.
                # Score is shown on the result image, together with the class label.
                detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
                detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
                num_detections = detection_graph.get_tensor_by_name('num_detections:0')

                base64ImgString = input_df['image base64 string'][0]
                pil_img = base64ToPilImg(base64ImgString)
                image_np = load_image_into_numpy_array(pil_img)
                
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(image_np, axis=0)
                # Actual detection.
                (boxes, scores, classes, num_detections) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})
                # ## Loading label map
                # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
                #PATH_TO_LABELS = "label_map.pbtxt"
                # label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
                # categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=FLAGS.nclasses, use_display_name=True)
                # category_index = label_map_util.create_category_index(categories)
                category_index={1: {'id': 1, 'name': 'laptop'}, 2: {'id': 2, 'name': 'person'}}
                boxes, scores, classes, num_detections = map(np.squeeze, [boxes, scores, classes, num_detections])

                results = []

                for i in range(int(num_detections)):
                    if scores[i] < 0.05:
                        continue
                    left, right, top, bottom = process_bounding_box(boxes[i])
                    res_class = category_index[classes[i]]
                    results.append([left, right, top, bottom, res_class])

                return '{"output":' + '"'  + json.dumps(results) + '"}'
    except Exception as e:
        return(str(e))

def main():
    from azureml.api.schema.dataTypes import DataTypes
    from azureml.api.schema.sampleDefinition import SampleDefinition
    from azureml.api.realtime.services import generate_schema
    import pandas

    # Create random 5x5 pixels image to use as sample input
    #base64ImgString = "iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAIAAAACDbGyAAAAFElEQVR4nGP8//8/AxJgYkAFpPIB6vYDBxf2tWQAAAAASUVORK5CYII="
    #pilImg = pilImread("C:/Users/pabuehle/Desktop/vienna/iris4/tiny.jpg")
    with open('sample.json') as f:
        jsonsample = json.load(f)

    # Call init() and run() function
    init()
    # df = create_df_from_json(jsonsample)
    # inputs = {"input_json": SampleDefinition(DataTypes.STANDARD, yourinputjson)}
    # resultString = run(df)
    # print("resultString = " + str(resultString))

    # # Genereate the schema
    # generate_schema(run_func=run, inputs=inputs, filepath='service_schema.json')
    # print("Schema generated.")

if __name__ == "__main__":
    main()
