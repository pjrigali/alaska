import re


def load_turnout(file_lst, repo) -> dict:
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
                    final_dic['20'] = male_female_unknown(lst=lst)
                elif '21' in lst[0].split(' ')[0]:
                    final_dic['21'] = male_female_unknown(lst=lst)
                elif ' THRU ' in lst[0]:
                    key = ' '.join(lst[0].split(' ')[:3])
                    final_dic[key] = male_female_unknown(lst=lst)
                elif 'ABOVE' in lst[0].split(' ')[0]:
                    final_dic['ABOVE 75'] = male_female_unknown(lst=lst)
                elif 'TOTALS' in lst[0].split(' ')[0]:
                    final_dic['TOTALS'] = male_female_unknown(lst=lst)
            turn_out_dic[year] = final_dic
    return turn_out_dic

def load_election(file_lst, repo) -> dict:
    dic = {}
    for file in file_lst:
        year = str(file.split('.')[0])
        with open(repo + '\\' + file, 'r') as f:
            lines = f.read().splitlines()
            dic[year] = [line.replace('"', '').split(',') for line in lines]
    return dic

def load_age(file_lst, repo) -> dict:
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
                final_dic[line[0]] = dict(zip(['Total', 'Male', 'Female', 'Unknown'], temp_lst))
            dic[year] = final_dic
    return dic
