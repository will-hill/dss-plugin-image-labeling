import dataiku
from flask import request
from base64 import b64encode
from dataiku.customwebapp import *

dataset_name = get_webapp_config()["dataset"]
folder_id = get_webapp_config()["folder"]

dataset = dataiku.Dataset(dataset_name)
folder = dataiku.Folder(folder_id)

current_schema_columns = [c['name'] for c in dataset.read_schema()]
if 'path' not in current_schema_columns or 'class' not in current_schema_columns or 'comment' not in current_schema_columns:
    raise ValueError("The target dataset should have a columns: 'path', 'class' and 'comment'")

try:
    current_df = dataset.get_dataframe()
except:
    print("Dataset probably empty")
    current_df = pd.DataFrame(columns=current_schema_columns, index=[])
    
labelled = set(current_df['path'])
all_paths = set(folder.list_paths_in_partition())
remaining = all_paths - labelled

@app.route('/get-image-base64')
def get_image():
    path = request.args.get('path')
    print('path: ' +str(path))
    with folder.get_download_stream(path) as s:
        data = b64encode(s.read())
    return json.dumps({"status": "ok", "data": data})

@app.route('/next')
def next():
    global current_df, all_paths, labelled, remaining
    return json.dumps({"status": "ok", "nextPath": getNextPath(), "labelled": len(labelled), "total": len(all_paths), "skipped": len(all_paths) - len(labelled) - len(remaining) - 1}) # -1 because the current is not counted

@app.route('/classify')
def classify():
    global current_df, all_paths, labelled, remaining
    path = request.args.get('path')
    cat = request.args.get('cat')
    comment = request.args.get('comment')
    
    current_df = current_df.append({'path': path, 'class': cat, 'comment': comment}, ignore_index=True)
    dataset.write_with_schema(current_df)
    labelled.add(path)
    return json.dumps({"status": "ok", "nextPath": getNextPath(), "labelled": len(labelled), "total": len(all_paths), "skipped": len(all_paths) - len(labelled) - len(remaining) - 1}) # -1 because the current is not counted

def getNextPath():
    if len(remaining) > 0:
        return remaining.pop()
    else:
        return None