import streamlit as st
import pandas as pd

st.title('Alaskan Voting Dashboard')
st.markdown('*This is a proof of concept demo.*')
st.markdown('This is a dashboard to showcase the potential impact of implementing online voting for the state of Alaska.')
st.markdown('The high level inovation includes distributed ledger technology to speed up the legacy process, ensure accuracy and provide operational cost efficencies.')

st.sidebar.title("Description:")
st.sidebar.markdown("This is a dashboard for maniplulating Alaskan voting data.")
st.sidebar.title("How to Use:")
st.sidebar.markdown("1. Select the desired Analysis")
st.sidebar.markdown("2. Select desired Gender Status or Year")
st.sidebar.markdown("*For best Results use 'Both' and 'All'.*")
st.sidebar.markdown("3. Clarify more specific data")
st.sidebar.title("Future Work:")
st.sidebar.markdown(" - Gender breakdowns")
st.sidebar.markdown(" - Party affilation")
st.sidebar.markdown("*Peter Rigali with Group 22 (Dream Team)*")
st.sidebar.write("[link]https://github.com/pjrigali/alaska")

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
select = st.selectbox('Desired Analysis', ['...', 'Who Votes?', 'What Ages are Represented?', 'What is the Potential Impact?'])

# Registered Verse Turnout
if select == 'Who Votes?':
    st.header('2.  Turnout Ratio')
    st.markdown("Comparing registered voters to election vote tally.")
    default = st.selectbox(label='2.1.  Gender', options=['Total', 'Female', 'Male', 'Unspecified'])
    pre_post = st.selectbox('2.2.  Status', ['Both', 'Registered', 'Voted'])
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
elif select == 'What Ages are Represented?':
    st.header("2.  Age Representation")
    year = st.selectbox('2.1.  Year', ['All', '2012', '2014', '2016', '2018', '2020'])
    temp_df = age_df[(age_df['Age'] != 'TOTAL') & (age_df['Age'] != 'UNKNOWN')][['Total', 'Age', 'Year']].set_index('Year')
    if year != 'All':
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').loc[year]
    else:
        df = pd.pivot_table(temp_df, values='Total', index='Year', columns='Age').sum()
    st.bar_chart(df)
    st.header('3.  Age related to Total:')
    st.markdown('*Here we are examining different combinations of age groups and returning the percent.*')
    ages = st.multiselect('Ages', age_lst_min, ['18 THRU 19', '_20_', '_21_', '22 THRU 24'])
    if year != 'All':
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age').loc[year]
        if ratio_df[ages].empty is False:
            st.dataframe(ratio_df[ages])
            val = round((sum(ratio_df[ages].tolist()) / int(ratio_df['TOTAL'])) * 100, 1)
            col1, col2, col3 = st.columns(3)
            col1.metric(year, str(val) + ' %')
    else:
        ratio_df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        if ratio_df[ages].empty is False:
            lst = ((ratio_df[ages].sum(axis=1) / ratio_df['TOTAL']) * 100).round(1).tolist()
            st.dataframe(pd.DataFrame(lst, index=['2012', '2014', '2016', '2018', '2020'], columns=['Percent']))

    over_time = st.selectbox('3.1.  Show chart over time?', ['Yes', 'No'])
    if over_time == 'Yes':
        ages_n = st.multiselect('Ages', age_lst, ['18 THRU 19', '_20_', '_21_', '22 THRU 24'])
        df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')
        dfn = pd.DataFrame(index=df.index)
        for i in ages_n:
            dfn[i] = df[i].tolist()
        st.line_chart(dfn)
        show = st.selectbox('Show Data', ['No', 'Yes'])
        if show == 'Yes':
            st.dataframe(dfn)

elif select == 'What is the Potential Impact?':
    st.header('2.  Forecasting')
    st.markdown('*Looking into the future.*')
    per = st.slider('Impact Percent', -0.5, 0.5, .10, .05)
    st.markdown('*Select Estimated Implementation Percent*')
    ages = st.multiselect('Ages', age_lst_min, ['18 THRU 19', '_20_', '_21_', '22 THRU 24'])
    st.markdown('*Select Ages to be affected by the implementation*')
    ages_dic = {i: True for i in ages}
    df = pd.pivot_table(age_df, values='Total', index='Year', columns='Age')[age_lst_min]
    expected = df.mean()
    increase = expected * per
    new_vals = {}
    for i in list(df.columns):
        if i not in ages_dic:
            new_vals[i] = expected[i]
        else:
            new_vals[i] = expected[i] + increase[i]
    new_line = pd.DataFrame(new_vals, index=['2022']).round(1)
    forecast = pd.concat([df, new_line])

    st.line_chart(forecast)

    val = df.loc['2020'].sum()
    val1 = sum(expected.tolist())
    val2 = sum(new_vals.values())
    val3 = (val1 - val) / val
    val4 = (val2 - val) / val

    col1, col2 = st.columns(2)
    col1.metric('Expected Voter Count Forecast', int(val1))
    col2.metric('Expected Percent Change', round(val3 * 100, 1))

    col3, col4 = st.columns(2)
    col3.metric('Implementation Voter Count Forecast', int(val2))
    col4.metric('Implementation Percent Change', round(val4 * 100, 1))

    show = st.selectbox('Show Data', ['No', 'Yes'])
    if show == 'Yes':
        st.dataframe(forecast)

