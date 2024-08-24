import streamlit as st
import pandas as pd
from datetime import datetime
import os

# File path for the cattle health CSV
file_path = 'cattle_health.csv'

# Create the CSV file if it doesn't exist
if not os.path.exists(file_path):
    df = pd.DataFrame(columns=['ID', 'Name', 'Age', 'Health Status', 'Last Checkup Date', 'Notes'])
    df.to_csv(file_path, index=False)

# Load cattle health data
def load_data():
    return pd.read_csv(file_path)

# Save cattle health data
def save_data(df):
    df.to_csv(file_path, index=False)

# Initialize Streamlit app
st.title('Cattle Health Management App')

# Load data into session state
if 'df' not in st.session_state:
    st.session_state.df = load_data()

# Display cattle health records
st.subheader('Cattle Health Records')
st.dataframe(st.session_state.df)

# Add new cattle health record
st.subheader('Add New Cattle Health Record')
cattle_id = st.text_input('ID')
name = st.text_input('Name')
age = st.number_input('Age', min_value=0, step=1)
health_status = st.selectbox('Health Status', ['Healthy', 'Sick', 'Recovering'])
last_checkup_date = st.date_input('Last Checkup Date')
notes = st.text_area('Notes')
if st.button('Add Record'):
    new_record = pd.DataFrame([{
        'ID': cattle_id,
        'Name': name,
        'Age': age,
        'Health Status': health_status,
        'Last Checkup Date': last_checkup_date.strftime('%Y-%m-%d'),
        'Notes': notes
    }])
    st.session_state.df = pd.concat([st.session_state.df, new_record], ignore_index=True)
    save_data(st.session_state.df)
    st.success('Record added successfully!')

# Update cattle health record
st.subheader('Update Cattle Health Record')
record_to_update = st.selectbox('Select Record to Update', st.session_state.df.index)
new_name = st.text_input('New Name', value=st.session_state.df.at[record_to_update, 'Name'])
new_age = st.number_input('New Age', min_value=0, step=1, value=st.session_state.df.at[record_to_update, 'Age'])
new_health_status = st.selectbox('New Health Status', ['Healthy', 'Sick', 'Recovering'], index=['Healthy', 'Sick', 'Recovering'].index(st.session_state.df.at[record_to_update, 'Health Status']))
new_last_checkup_date = st.date_input('New Last Checkup Date', value=datetime.strptime(st.session_state.df.at[record_to_update, 'Last Checkup Date'], '%Y-%m-%d'))
new_notes = st.text_area('New Notes', value=st.session_state.df.at[record_to_update, 'Notes'])
if st.button('Update Record'):
    st.session_state.df.at[record_to_update, 'Name'] = new_name
    st.session_state.df.at[record_to_update, 'Age'] = new_age
    st.session_state.df.at[record_to_update, 'Health Status'] = new_health_status
    st.session_state.df.at[record_to_update, 'Last Checkup Date'] = new_last_checkup_date.strftime('%Y-%m-%d')
    st.session_state.df.at[record_to_update, 'Notes'] = new_notes
    save_data(st.session_state.df)
    st.success('Record updated successfully!')

# Remove cattle health record
st.subheader('Remove Cattle Health Record')
record_to_remove = st.selectbox('Select Record to Remove', st.session_state.df.index)
if st.button('Remove Record'):
    st.session_state.df = st.session_state.df.drop(record_to_remove)
    save_data(st.session_state.df)
    st.success('Record removed successfully!')
