import json

data = {
    'id': ['Vasya266', {'age':17, 'last_visit':'18.04.2006', 'all_time':'20 hours'}]

}

with open('infomation.json', 'w') as j_file:
    json.dump(data, j_file)