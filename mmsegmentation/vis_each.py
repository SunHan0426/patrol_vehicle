import os
import re
import csv

class_list = ['background', 'PR', 'PA', 'PBS']
log_path = 'path/to/log'
output_folder = 'path/to/save'

def transform_table_line(raw):
    raw = list(map(lambda x: x.split('|'), raw))
    raw = list(map(
        lambda row: list(map(
            lambda col: float(col.strip()),
            row
        )),
        raw
    ))
    return raw

with open(log_path, 'r') as f:
    logs = f.read()

metrics_json = {}

for each_class in class_list:
    re_pattern = r'\s+{}.*?\|(.*)?\|'.format(each_class)
    metrics_json[each_class] = {}
    metrics_json[each_class]['re_pattern'] = re.compile(re_pattern)

for each_class in class_list:
    find_string = re.findall(metrics_json[each_class]['re_pattern'], logs)

    find_string = transform_table_line(find_string)

    metrics_json[each_class]['metrics'] = find_string

    csv_file_path = os.path.join(output_folder, '{}.csv'.format(each_class))

    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['IoU', 'Acc', 'Dice', 'Fscore', 'Precision', 'Recall'])
        for row in find_string:
            writer.writerow(row)
