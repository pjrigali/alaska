import streamlit as st
import pandas as pd

st.title('Alaska Voting Dashboard')
st.markdown('*This is a proof of concept demo.*')

# st.sidebar.title("Description:")
# st.sidebar.markdown("This is a web application version of the Cold-War-Zombies python package. The python version allows you to have multiples of the same weapon.")
# st.sidebar.title("How to Use:")
# st.sidebar.markdown("1. Select the desired zombie round")
# st.sidebar.markdown("2. Select desired weapons for comparison")
# st.sidebar.markdown("3. Select the desired weapon attachments")
# st.sidebar.markdown("4. View comparison tables below")
# st.sidebar.title("Weapons:")
# st.sidebar.markdown("*All weapons are included up until mid-season 6.*")

turn_df = pd.read_csv('./data/turn.csv', index_col='Unnamed: 0')
election_df = pd.read_csv('./data/election.csv', index_col='Unnamed: 0')
age_df = pd.read_csv('./data/age.csv', index_col='Unnamed: 0', dtype={'Age': 'str', 'Year': 'str'})
age_lst = ['18 THRU 19', '_20_', '_21_', '22 THRU 24', '25 THRU 34', '35 THRU 44', '45 THRU 54', '55 THRU 59',
           '60 THRU 61', '62 THRU 64', '65 THRU 74', 'ABOVE 75', 'TOTAL']

st.header('Select Desired Viz')
select = st.selectbox('Desired Analysis', ['...', 'Who commits to Voting?', 'What Age is Represented?'])


# Registered Verse Turnout
if select == 'Who commits to Voting?':
    st.header('Turnout Ratio')
    st.markdown("Here we are comparing the amount of registed voters to those who actually show.")
    default = st.selectbox('Gender', ['Female', 'Male', 'Unspecified', 'Total'])
    pre_post = st.selectbox('Status', ['Registered', 'Voted', 'Both'])
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

elif select == 'What Age is Represented?':
    year = st.selectbox('Year', ['2012', '2014', '2016', '2018', '2020', 'All'])
    temp_df = age_df[(age_df['Age'] != 'TOTAL') & (age_df['Age'] != 'UNKNOWN')][['Total', 'Age', 'Year']].set_index('Year')
    if year != 'All':
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').loc[year]
    else:
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').sum()
    st.bar_chart(df)

    ages = st.multiselect('Ages', age_lst)
    if year != 'All':
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age').loc[year]
        st.dataframe(ratio_df[ages])
        val = sum(ratio_df[ages].tolist()) / ratio_df['TOTAL'].value
        col1, co32, col3 = st.columns(3)
        col1.metric(year, str(val))
    else:
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        st.dataframe(ratio_df[ages])
        # st.dataframe(ratio_df.loc['TOTAL'])





    # st.dataframe(dfn)
    # col1 = st.columns(1)
    # col1.metric(year, str(sum([df[i] for i in ages]) / df['TOTAL']))


    over_time = st.selectbox('Over Time?', ['No', 'Yes'])
    if over_time == 'Yes':
        ages = st.multiselect('Ages', age_lst)
        df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        dfn = pd.DataFrame()
        for i in ages:
            dfn[i] = df[i].tolist()
        st.line_chart(dfn)
        show = st.selectbox('Show Data', ['No', 'Yes'])
        if show == 'Yes':
            st.dataframe(dfn)


