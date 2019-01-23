from dataiku import Dataset

def do(payload, config, plugin_config, inputs):
    if 'check_dataset' in payload:
        dataset_name = config.get('dataset', None)
        if dataset_name is None:
            return {"ok":False, "reason":"No dataset selected"}
        else:
            dataset = dataiku.Dataset(dataset_name)
            schema = dataset.read_schema()
            columns = set([c['name'] for c in schema])
            needed = set(['class', 'path', 'comment'])
            missing = needed - columns
            if len(missing) == 0:
                return {"ok":True}
            else:
                return {"ok":False, "reason":"Missing columns %s" % ','.join(missing)}
    else:
        return {}
