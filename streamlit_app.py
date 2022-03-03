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
pre_post = st.selectbox('Default', ['Registered', 'Voted', 'Both'])

if default is 'Unspecified':
    default = 'Unknown'

if pre_post in {'Registered': True, 'Voted': True}:
    if default is 'Total':
        df = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] ==  pre_post)][['Year', 'Female', 'Male', 'Unknown']].set_index('Year').sum(axis=1)
    else:
        df = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == pre_post)][['Year', default]].set_index('Year')
else:
    if default is 'Total':
        df1 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Voted')][
            ['Year', 'Female', 'Male', 'Unknown']].set_index('Year').sum(axis=1)
        df2 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Registered')][
            ['Year', 'Female', 'Male', 'Unknown']].set_index('Year').sum(axis=1)
        df = pd.concat([df1, df2], axis=1)
        df.columns = ['Voted', 'Registered']
        # df = turn_df[(turn_df['Age'] == 'TOTALS')][['Year', 'Female', 'Male', 'Unknown']].set_index('Year').sum(
        #     axis=1)
        # col_lst = []
        # cols = {}
        # for i in list(df.index):
        #     if i not in cols:
        #         cols[i] = True
        #         col_lst.append(str(i) + '_Registered')
        #     else:
        #         col_lst.append(str(i) + '_Voted')
        # df.index = col_lst
        # df = pd.DataFrame([df.tolist()], columns=col_lst, index=[0])

        # df = turn_df[(turn_df['Age'] == 'TOTALS')][['Year', 'Female', 'Male', 'Unknown']].set_index('Year').T
        # col_lst = []
        # cols = {}
        # for i in df.columns:
        #     if i not in cols:
        #         cols[i] = True
        #         col_lst.append(str(i) + '_Registered')
        #     else:
        #         col_lst.append(str(i) + '_Voted')
        # df.columns = col_lst
    else:
        # df = turn_df[(turn_df['Age'] == 'TOTALS')][['Year', default]].set_index('Year')
        df1 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Voted')][
            ['Year', default]].set_index('Year')
        df1.columns = ['Voted']
        df2 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Registered')][
            ['Year', default]].set_index('Year')
        df2.columns = ['Registered']
        df = pd.concat([df1, df2], axis=1)
st.bar_chart(df)