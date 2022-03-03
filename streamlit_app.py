import streamlit as st
import pandas as pd

st.title('Alaska Voting Dashboard')
st.markdown('*This is a proof of work demo.*')

st.sidebar.title("Description:")
st.sidebar.markdown("This is a web application version of the Cold-War-Zombies python package. The python version allows you to have multiples of the same weapon.")
st.sidebar.title("How to Use:")
st.sidebar.markdown("1. Select the desired zombie round")
st.sidebar.markdown("2. Select desired weapons for comparison")
st.sidebar.markdown("3. Select the desired weapon attachments")
st.sidebar.markdown("4. View comparison tables below")
st.sidebar.title("Weapons:")
st.sidebar.markdown("*All weapons are included up until mid-season 6.*")

turn_df = pd.read_csv('./data/turn.csv', index_col='Unnamed: 0')
election_df = pd.read_csv('./data/election.csv', index_col='Unnamed: 0')
age_df = pd.read_csv('./data/age.csv', index_col='Unnamed: 0')

# Registered Verse Turnout
st.header('Comparing Registered and Voting Numbers')
default = st.selectbox('Default', ['Female', 'Male', 'Unspecified', 'Total'])
pre_post = st.selectbox['Default', ['Registered', 'Voted']]

if default is 'Unspecified':
    default = 'Unknown'

df = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == pre_post)][['Year', default]].set_index('Year')
st.bar_chart(df)