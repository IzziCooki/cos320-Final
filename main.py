import json

def read_json_file(file_path):
    ids = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)

            if data['state'].upper() == 'FL':
                ids.append(data['name'])
    print(ids)
            
def get_business_data_by_state(file_path, state):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            d = json.loads(line)
            if d['state'].upper() == state:
                data.append(d)
    return data

print(get_business_data_by_state('Final/data/yelp_academic_dataset_business.json', 'FL'))