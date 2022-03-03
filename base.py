import re
import os
import pandas as pd


def load_turnout(file_lst, repo) -> pd.DataFrame:
    turn_out_dic = {}
    for file in file_lst:
        year = str(file.split('.')[0])
        with open(repo + '\\' + file, 'r') as f:
            lines = f.read().splitlines()
            line_lst = []
            temp_lst = []
            voted = False
            for line in lines:
                temp_lst.append(line)
                if 'VOTED' in line:
                    voted = True
                if 'UNKNOWN GENDER' in line and voted is True:
                    line_lst.append(temp_lst)
                    temp_lst = []
                    voted = False

            def male_female_unknown(lst):
                unknown_dic = {'Registered': {}, 'Voted': {}}
                first = True
                for line in lst:
                    if 'MALE' in line and 'FEMALE' not in line:
                        vals = sum([float(i) for i in line.split('MALE ')[1].split(' ')][2:])
                        if first is True:
                            unknown_dic['Registered']['Male'] = vals
                        else:
                            unknown_dic['Voted']['Male'] = vals
                    elif 'FEMALE ' in line:
                        vals = sum([float(i) for i in line.split('FEMALE ')[1].split(' ')][2:])
                        if first is True:
                            unknown_dic['Registered']['Female'] = vals
                        else:
                            unknown_dic['Voted']['Female'] = vals
                    elif 'UNKNOWN GENDER ' in line:
                        vals = sum([float(i) for i in line.split('UNKNOWN GENDER ')[1].split(' ')][2:])
                        if first is True:
                            unknown_dic['Registered']['Unknown'] = vals
                        else:
                            unknown_dic['Voted']['Unknown'] = vals
                    elif 'VOTED ' in line:
                        first = False
                return unknown_dic

            final_dic = {}
            for lst in line_lst:
                if 'UNKNOWN DOB' in lst[0]:
                    final_dic['UNKNOWN DOB'] = male_female_unknown(lst=lst)
                elif '20' in lst[0].split(' ')[0]:
                    final_dic['_20_'] = male_female_unknown(lst=lst)
                elif '21' in lst[0].split(' ')[0]:
                    final_dic['_21_'] = male_female_unknown(lst=lst)
                elif ' THRU ' in lst[0]:
                    key = ' '.join(lst[0].split(' ')[:3])
                    final_dic[key] = male_female_unknown(lst=lst)
                elif 'ABOVE' in lst[0].split(' ')[0]:
                    final_dic['ABOVE 75'] = male_female_unknown(lst=lst)
                elif 'TOTALS' in lst[0].split(' ')[0]:
                    final_dic['TOTALS'] = male_female_unknown(lst=lst)
            turn_out_dic[year] = final_dic

    lst = []
    for i in ['2016', '2018', '2020']:
        temp_lst = []
        for key, val in turn_out_dic[i].items():
            for key1, val1 in val.items():
                temp_dic = {'Year': i, 'Age': key, 'Pre or Post': key1, 'Male': int(val1['Male']),
                            'Female': int(val1['Female']), 'Unknown': int(val1['Unknown'])}
                lst.append(temp_dic)
    return pd.DataFrame(lst)

def load_election(file_lst, repo) -> pd.DataFrame:
    remove_line_dic = {'Race Statistics': True, 'Number of Precincts for Race': True,
                       'Number of Precincts Reporting': True, 'Registered Voters': True,
                       'Times Counted': True}
    length = {'2014': 6, '2016': 6, '2018': 5, '2020': 5}
    dic = {}
    for file in file_lst:
        year = str(file.split('.')[0])
        with open(repo + '\\' + file, 'r') as f:
            lines = f.read().splitlines()
            temp_vals = [line.replace('"', '').split(',') for line in lines]
            vals = []
            for line in temp_vals:
                include = True
                line_lst = []
                for val in line:
                    temp_val = val.strip()
                    if temp_val in remove_line_dic:
                        include = False
                        break
                    if temp_val != 'Total' and len(val) > 0 and temp_val != 'NP':
                        line_lst.append(temp_val)
                if include and len(line_lst) == length[year]:
                    if year in {'2014': True, '2016': True}:
                        line_lst = [line_lst[0], line_lst[1], line_lst[2] + '/' + line_lst[3], line_lst[4], int(line_lst[5])]
                    vals.append(line_lst)
            dic[year] = vals

    lst = []
    for i in ['2014', '2016', '2018', '2020']:
        temp_df = pd.DataFrame(dic[i], columns=['Precinct', 'Position', 'Name', 'Party', 'Votes'])
        temp_df['Year'] = i
        lst.append(temp_df)
    return pd.concat(lst).reset_index(drop=True)

def load_age(file_lst, repo) -> pd.DataFrame:
    dic = {}
    for file in file_lst:
        year = str(file.split('.')[0])
        with open(repo + '\\' + file, 'r') as f:
            lines = f.read().splitlines()
            lst = [re.split(r'\t+', line) for line in lines[1:]]
            final_dic = {}
            for line in lst:
                temp_lst = []
                for val in line[1:5]:
                    temp_lst.append(int(''.join([ch for ch in val if ch.isdigit()])))
                key = line[0]
                if ' AND ' in key:
                    key = key.replace('AND', 'THRU')
                elif '20' in key or '21' in key:
                    key = '_' + key + '_'
                final_dic[key] = dict(zip(['Total', 'Male', 'Female', 'Unknown'], temp_lst))
            dic[year] = final_dic

    lst = []
    for i in ['2012', '2014', '2016', '2018', '2020']:
        t = pd.DataFrame.from_dict(dic[i], orient='index').reset_index()
        t['Year'] = i
        t.columns = ['Age', 'Total', 'Male', 'Female', 'Unknown', 'Year']
        lst.append(t)

    return pd.concat(lst).reset_index(drop=True)

def load_data():
    turn_out_repo = 'data\\Turn Out'
    election_repo = 'data\\Election'
    age_repo = 'data\\Age'
    turn_out = next(os.walk(turn_out_repo))[2]
    # turn_out = ['2016.txt', '2018.txt', '2020.txt']
    election = next(os.walk(election_repo))[2]
    # election = ['2014.txt', '2016.txt', '2018.txt', '2020.txt']
    age = next(os.walk(age_repo))[2]
    # age = ['2012.txt', '2014.txt', '2016.txt', '2018.txt', '2020.txt']
    turn_out_dic = load_turnout(file_lst=turn_out, repo=turn_out_repo)
    election_dic = load_election(file_lst=election, repo=election_repo)
    age_dic = load_age(file_lst=age, repo=age_repo)
    return turn_out_dic, election_dic, age_dic
