from dataiku.customwebapp import *

import dataiku
from dataiku.core import schema_handling
from flask import request
from base64 import b64encode
import pandas as pd
import numpy as np
import re


if "objects" not in get_webapp_config():
    raise ValueError("Objects folder not specified. Go to settings tab.")
if "frames" not in get_webapp_config():
    raise ValueError("Frames folder not specified. Go to settings tab.")
if "dataset" not in get_webapp_config():
    raise ValueError("Output dataset not specified. Go to settings tab.")

dataset_name = get_webapp_config()["dataset"]
objects_id = get_webapp_config()["objects"]
frames_id = get_webapp_config()["frames"]

dataset = dataiku.Dataset(dataset_name)
objects = dataiku.Folder(objects_id)
frames = dataiku.Folder(frames_id)

try:
    current_schema = dataset.read_schema()
    current_schema_columns = [c['name'] for c in current_schema]
except:
    current_schema_columns = ["path", "class", "comment"]
    dataset.write_schema([{"name": "path", "type": "string"}, {"name": "class", "type": "string"}, {"name": "comment", "type": "string"}])
    
if 'path' not in current_schema_columns or 'class' not in current_schema_columns or 'comment' not in current_schema_columns:
    raise ValueError("The target dataset should have columns: 'path', 'class' and 'comment'. Please edit the schema in the dataset settings.")

try:
    current_df = dataset.get_dataframe()
except:
    print("Dataset probably empty")
    current_df = pd.DataFrame(columns=current_schema_columns, index=[])
    for col in current_schema:
        n = col["name"]
        t = col["type"]
        t = schema_handling.DKU_PANDAS_TYPES_MAP.get(t, np.object_)
        current_df[n] = current_df[n].astype(t)
    
labelled = set(current_df['path'])
all_paths = set(objects.list_paths_in_partition())
remaining = all_paths - labelled

@app.route('/get-frame')
def get_frame():
    path = request.args.get('path')
    path = re.sub('_score_\d+\.\d+\.png','.png',path).replace('cropped_','scored_')
    with frames.get_download_stream(path) as s:
        data = b64encode(s.read())
    return json.dumps({"data": data})

@app.route('/get-image-base64')
def get_image():
    path = request.args.get('path')
    with objects.get_download_stream(path) as s:
        data = b64encode(s.read())
    return json.dumps({"data": data})

@app.route('/next')
def next():
    global current_df, all_paths, labelled, remaining
    if len(remaining) > 0:
        next_path = remaining.pop()
    else:
        next_path = None
    total_count = len(all_paths)
    skipped_count = len(all_paths) - len(labelled) - len(remaining) - 1 # -1 because the current is not counted
    labelled_count = len(labelled)
    by_category = current_df['class'].value_counts().to_dict()
    return json.dumps({"nextPath": next_path, "labelled": labelled_count, "total": total_count, "skipped": skipped_count, "byCategory" : by_category}) 

@app.route('/classify')
def classify():
    global current_df, all_paths, labelled, remaining

    print('CLASSIFY')
    
    print('current_df.shape: ' + str(current_df.shape[0]) + ' by ' + str(current_df.shape[1]))
    
    path = request.args.get('path')
    print('path: ' + path)
    
    cat = request.args.get('category')
    print('cat: ' + cat)
    
    comment = request.args.get('comment')
    print('comment: ' + comment)    
    
    print('APPENDING....')
    current_df = current_df.append({'path': path, 'class': cat, 'comment': comment}, ignore_index=True)

    print('WRITE....')
    dataset.write_from_dataframe(current_df)
    
    print('CLASSIFY - 7')    
    labelled.add(path)
    print('CLASSIFY - 8')    
    return next()







