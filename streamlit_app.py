import streamlit as st
from base import load_data
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


turn_out, election, age = load_data()