import os
from base import load_data
import pandas as pd

# Load and Build Data
turn_out, election, age = load_data()

# Save Data
for key, val in {'turn.csv': turn_out,'election.csv': election,'age.csv': age}.items():
    val.to_csv('data\\' + key, header=True)
