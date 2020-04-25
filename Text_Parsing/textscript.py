import re  # regex

import pandas as pd

rx_dict = {
    'query_id': re.compile(r"(?P<query_id>AU=([^,])+)"),
    'daisng_id': re.compile(r"daisng_id: (?P<daisng_id>([^,])+)"),
    'role': re.compile(r"role: (?P<role>([^,])+)"),
    'seq_no': re.compile(r"seq_no: (?P<seq_no>([^,])+)"),
    'display_name': re.compile(r"display_name: (?P<display_name>([^,],[^,](\w+)))"),
    'full_address': re.compile(r"full_address: (?P<full_address>([^,],[^,],[^,],[^,](\w+)))"),
    'organization': re.compile(r"organization: (?P<organization>([^,])+)"),
    'city': re.compile(r"city: (?P<city>([^,])+)"),
    'country': re.compile(r"country: (?P<country>([^\}])+)"),
    'uid': re.compile(r"(?P<uid>WOS:.+)\n")
}


def _parse_line(line):
    pd_data = {}
    for key, rx in rx_dict.items():
        listed = []
        for match in rx.finditer(line):
            listed.append(match.group(1))
        pd_data[key] = listed
    return pd_data


def parse_file(filepath):
    data = []  # create an empty list to collect the data
    # open the file and read through it line by line
    global a
    with open(filepath, 'r') as file_object:
        next(file_object)
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            keys = _parse_line(line)
            # extract query_id
            if keys['query_id']:
                query_id = keys['query_id']
            # extract daisng_id
            if keys['daisng_id']:
                daisng_id = keys['daisng_id']
            # extract role
            if keys['role']:
                role = keys['role']
            # extract uid
            if keys['uid']:
                uid = keys['uid']
            # extract seq_no
            if keys['seq_no']:
                seq_no = keys['seq_no']
            # extract display_name
            if keys['display_name']:
                display_name = keys['display_name']
            # extract full_address
            if keys['full_address']:
                full_address = keys['full_address']
            if keys['organization']:
                organization = keys['organization']
            if keys['city']:
                city = keys['city']
            # extract country
            if keys['country']:
                country = keys['country']
                # read each line of the table until a blank line
            row = {
                'uid': uid,
                'display_name': display_name,
                'daisng_id': daisng_id,
                'role': role,
                'seq_no': seq_no,
                'full_address': full_address,
                'organization': organization,
                'city': city,
                'country': country,
                'query_id': query_id,
            }
            # append the dictionary to the data list
            data.append(row)
            a = data
            line = file_object.readline()

        column_names = ['uid', 'display_name', 'daisng_id', 'role', 'seq_no', 'full_address',
                        'organization', 'city', 'country', 'query_id']
        df = pd.DataFrame(columns=column_names)
        for element in data:
            data = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in element.items()]))
            data = data.fillna(method='ffill')
            df = df.append(data)
    return df


filepath = 'tobe_parsed.csv'

with open(filepath, 'r') as file_object:
    content = file_object.read()
# remove single and double quotation marks
with open(filepath, 'w') as file_object:
    file_object.write(content.replace('\'', ''))

data = parse_file(filepath)
print(data)  # print parsed data on the secreen
# save parsed data as csv file
data.to_csv(r'..\Desktop\parsed_data.csv', index=False, header=True)