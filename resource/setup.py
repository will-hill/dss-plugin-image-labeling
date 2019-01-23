from dataiku import Dataset
from sets import Set

# paylaod is sent from the javascript's callPythonDo()
# config and plugin_config are the recipe/dataset and plugin configured values
# inputs is the list of input roles (in case of a recipe)
def do(payload, config, plugin_config, inputs):
    role_name = 'input_role'
    # get dataset name then dataset handle
    dataset_full_names = [i['fullName'] for i in inputs if i['role'] == role_name]
    if len(dataset_full_names) == 0:
        return {'choices' : []}
    dataset = Dataset(dataset_full_names[0])
    # get name of column providing the choices
    column_name = config.get('filterColumn', '')
    if len(column_name) == 0:
        return {'choices' : []}
    # check that the column is in the schema
    schema = dataset.read_schema()
    schema_columns = [col for col in schema if col['name'] == column_name]
    if len(schema_columns) != 1:
        return {'choices' : []}
    schema_column = schema_columns[0]
    # get the data and build the set of values
    choices = Set()
    for row in dataset.iter_tuples(sampling='head', limit=10000, columns=[column_name]):
        choices.add(row[0])
    return {'choices' : list(choices)}