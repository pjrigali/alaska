import os

from base import load_turnout, load_election, load_age

turn_out_repo = 'C:\\Users\\Peter\\Desktop\\Alaska\\Turn Out'
election_repo = 'C:\\Users\\Peter\\Desktop\\Alaska\\Election'
age_repo = 'C:\\Users\\Peter\\Desktop\\Alaska\\Age'

turn_out = next(os.walk(turn_out_repo))[2]
election = next(os.walk(election_repo))[2]
age = next(os.walk(age_repo))[2]

turn_out_dic = load_turnout(file_lst=turn_out, repo=turn_out_repo)
election_dic = load_election(file_lst=election, repo=election_repo)
age_dic = load_age(file_lst=age, repo=age_repo)

age_dic