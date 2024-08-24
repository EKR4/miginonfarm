import streamlit as st
import pandas as pd

from datetime import date

# Initialize session state for milk_data
if 'milk_data' not in st.session_state:
    try:
        st.session_state.milk_data = pd.read_csv('milk_production.csv', parse_dates=['Date'])
    except FileNotFoundError:
        st.session_state.milk_data = pd.DataFrame(columns=['Date', 'Cow Name', 'Morning', 'Noon', 'Evening'])

# Initialize Streamlit app
st.title('Milk Production Tracker')
# Function to update the DataFrame widget
def update_table():
    st.dataframe(st.session_state.milk_data)



# Create interactive widgets
date_picker = st.date_input('Date', value=date.today())
cow_name_input = st.text_input('Cow Name')
morning_input = st.number_input('Morning Production (L)', step=0.1)
noon_input = st.number_input('Noon Production (L)', step=0.1)
evening_input = st.number_input('Evening Production (L)', step=0.1)
selected_index = st.selectbox('Select Record to Edit/Delete', st.session_state.milk_data.index)

# Arrange buttons in a row format
col1, col2, col3 = st.columns(3)
with col1:
    add_button = st.button('Add Record', key='add_button')
with col2:
    edit_button = st.button('Edit Record', key='edit_button')
with col3:
    delete_button = st.button('Delete Record', key='delete_button')

# Function to add a new record to the DataFrame
def add_record():
    new_record = pd.DataFrame({
        'Date': [date_picker],
        'Cow Name': [cow_name_input],
        'Morning': [morning_input],
        'Noon': [noon_input],
        'Evening': [evening_input]
    })
    st.session_state.milk_data = pd.concat([st.session_state.milk_data, new_record], ignore_index=True)
    st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
    st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
    st.rerun()

# Function to edit a selected record in the DataFrame
def edit_record():
    st.session_state.milk_data.at[selected_index, 'Date'] = date_picker
    st.session_state.milk_data.at[selected_index, 'Cow Name'] = cow_name_input
    st.session_state.milk_data.at[selected_index, 'Morning'] = morning_input
    st.session_state.milk_data.at[selected_index, 'Noon'] = noon_input
    st.session_state.milk_data.at[selected_index, 'Evening'] = evening_input
    st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
    st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
    st.rerun()

# Function to delete a selected record from the DataFrame
def delete_record():
    st.session_state.milk_data = st.session_state.milk_data.drop(selected_index).reset_index(drop=True)
    st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
    st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
    st.rerun()

# Handle button clicks
if add_button:
    add_record()

if edit_button:
    edit_record()

if delete_button:
    delete_record()

# Display the DataFrame and plot
update_table()

# Custom CSS for button colors
st.markdown("""
    <style>
    .stButton > button[data-testid="add_button"] {
        background-color: #4CAF50; /* Green */
        color: white;
    }
    .stButton > button[data-testid="edit_button"] {
        background-color: #FFD700; /* Yellow */
        color: black;
    }
    .stButton > button[data-testid="delete_button"] {
        background-color: #FF0000; /* Red */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
