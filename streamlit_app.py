import streamlit as st
import pandas as pd

st.title('Alaska Voting Dashboard')
st.markdown('*This is a proof of concept demo.*')

st.sidebar.title("Description:")
st.sidebar.markdown("This is a dashboard for maniplulating alaska voting data")
st.sidebar.title("How to Use:")
st.sidebar.markdown("1. Select the desired Analysis")
st.sidebar.markdown("2. Select desired Gender Status or Year")
st.sidebar.markdown("*For best Results use 'Both' and 'All'.*")
st.sidebar.markdown("3. Clarify more specific data")
st.sidebar.title("Future Work:")
st.sidebar.markdown("Forecasting w/ sliders")
st.sidebar.markdown("Adoption Slider")
st.sidebar.markdown("More gender breakdowns")
st.sidebar.markdown("Party affilation")

# Load Data
turn_df = pd.read_csv('./data/turn.csv', index_col='Unnamed: 0')
election_df = pd.read_csv('./data/election.csv', index_col='Unnamed: 0')
age_df = pd.read_csv('./data/age.csv', index_col='Unnamed: 0', dtype={'Age': 'str', 'Year': 'str'})

# Helper Lists
age_lst = ['18 THRU 19', '_20_', '_21_', '22 THRU 24', '25 THRU 34', '35 THRU 44', '45 THRU 54', '55 THRU 59',
           '60 THRU 61', '62 THRU 64', '65 THRU 74', 'ABOVE 75', 'TOTAL']
age_lst_min = ['18 THRU 19', '_20_', '_21_', '22 THRU 24', '25 THRU 34', '35 THRU 44', '45 THRU 54', '55 THRU 59',
               '60 THRU 61', '62 THRU 64', '65 THRU 74', 'ABOVE 75']

# Start the page
st.header('1.  Select Desired Viz')
select = st.selectbox('Desired Analysis', ['...', 'Who commits to Voting?', 'What Age is Represented?'])

# Registered Verse Turnout
if select == '2.  Who commits to Voting?':
    st.header('Turnout Ratio')
    st.markdown("Here we are comparing the amount of registed voters to those who actually show.")
    default = st.selectbox('2.1: Gender', ['Female', 'Male', 'Unspecified', 'Total'])
    pre_post = st.selectbox('2.2: Status', ['Registered', 'Voted', 'Both'])
    st.markdown("If 'Both' is selected, ratios will be plotted.")

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
        else:
            df1 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Voted')][
                ['Year', default]].set_index('Year')
            df1.columns = ['Voted']
            df2 = turn_df[(turn_df['Age'] == 'TOTALS') & (turn_df['Pre or Post'] == 'Registered')][
                ['Year', default]].set_index('Year')
            df2.columns = ['Registered']
            df = pd.concat([df1, df2], axis=1)

    st.bar_chart(df)

    if pre_post == 'Both':
        st.header('Turnout Ratios')
        ratios = (df['Voted'] / df['Registered']).tolist()
        col1, col2, col3 = st.columns(3)
        col1.metric('2016', str(round(ratios[0] * 100, 1)) +' %')
        col2.metric('2018', str(round(ratios[1] * 100, 1)) + ' %')
        col3.metric('2020', str(round(ratios[2] * 100, 1)) + ' %')
        st.markdown('Above are the percentage of voters who actually showed up.')


# Age Group Overview
elif select == '2.  What Age is Represented?':
    year = st.selectbox('2.1.  Year', ['2012', '2014', '2016', '2018', '2020', 'All'])
    temp_df = age_df[(age_df['Age'] != 'TOTAL') & (age_df['Age'] != 'UNKNOWN')][['Total', 'Age', 'Year']].set_index('Year')
    if year != 'All':
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').loc[year]
    else:
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').sum()
    st.bar_chart(df)
    st.header('3.  Age related to Total:')
    st.markdown('*Here we are examining different combinations of age groups and returning the percent.*')
    ages = st.multiselect('Ages', age_lst_min)
    if year != 'All':
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age').loc[year]
        st.dataframe(ratio_df[ages])
        val = round((sum(ratio_df[ages].tolist()) / int(ratio_df['TOTAL'])) * 100, 1)
        col1, col2, col3 = st.columns(3)
        col1.metric(year, str(val) + ' %')
    else:
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        lst = ((ratio_df[ages].sum(axis=1) / ratio_df['TOTAL']) * 100).round(1).tolist()
        st.dataframe(pd.DataFrame(lst, index=['2012', '2014', '2016', '2018', '2020'], columns=['Percent']))

    over_time = st.selectbox('3.1.  Over Time?', ['No', 'Yes'])
    if over_time == 'Yes':
        ages_n = st.multiselect('Ages', age_lst)
        df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        dfn = pd.DataFrame()
        for i in ages_n:
            dfn[i] = df[i].tolist()
        st.line_chart(dfn)
        show = st.selectbox('Show Data', ['No', 'Yes'])
        if show == 'Yes':
            st.dataframe(dfn)
