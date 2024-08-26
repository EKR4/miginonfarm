import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Initialize session state for milk_data
if 'milk_data' not in st.session_state:
    try:
        st.session_state.milk_data = pd.read_csv('milk_production.csv', parse_dates=['Date'])
        if st.session_state.milk_data.empty:
            start_date_default = None
            end_date_default = None
        else:
            start_date_default = date.today() - timedelta(days=1)
            end_date_default = date.today()
    except FileNotFoundError:
        st.session_state.milk_data = pd.DataFrame(columns=['Date', 'Cow Name', 'Morning', 'Noon', 'Evening', 'Total'])
        st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Create the CSV file
        start_date_default = None
        end_date_default = None

# Ensure start_date_default and end_date_default are defined
if 'start_date_default' not in locals():
    start_date_default = date.today() - timedelta(days=1)
if 'end_date_default' not in locals():
    end_date_default = date.today()

# Initialize Streamlit app
st.title('Milk Production Tracker')

# Function to update the DataFrame widget
def update_table(filtered_data):
    st.dataframe(filtered_data)

# Function to get the highest milk producer for the filtered data
def get_highest_producer(filtered_data):
    try:
        if not filtered_data.empty:
            filtered_data['Total'] = filtered_data['Morning'] + filtered_data['Noon'] + filtered_data['Evening']
            highest_producer = filtered_data.loc[filtered_data['Total'].idxmax()]
            return highest_producer['Cow Name'], highest_producer['Total']
    except Exception as e:
        st.error(f"Error in get_highest_producer: {e}")
    return None, 0.0

# Function to get the total milk produced for the filtered data
def get_total_milk_produced(filtered_data):
    try:
        if not filtered_data.empty:
            filtered_data['Total'] = filtered_data['Morning'] + filtered_data['Noon'] + filtered_data['Evening']
            return filtered_data['Total'].sum()
    except Exception as e:
        st.error(f"Error in get_total_milk_produced: {e}")
    return 0

# Function to get the overall total milk produced
def get_overall_total_milk_produced():
    try:
        if not st.session_state.milk_data.empty:
            st.session_state.milk_data['Total'] = st.session_state.milk_data['Morning'] + st.session_state.milk_data['Noon'] + st.session_state.milk_data['Evening']
            return st.session_state.milk_data['Total'].sum()
    except Exception as e:
        st.error(f"Error in get_overall_total_milk_produced: {e}")
    return 0

# Create interactive widgets
start_date = st.date_input('Start Date', value=start_date_default)
end_date = st.date_input('End Date', value=end_date_default)

# Filter the DataFrame based on the selected date range
if start_date and end_date:
    filtered_data = st.session_state.milk_data[(st.session_state.milk_data['Date'] >= pd.to_datetime(start_date)) & (st.session_state.milk_data['Date'] <= pd.to_datetime(end_date))]
else:
    filtered_data = st.session_state.milk_data

# Create dashboard tiles
highest_producer, highest_production = get_highest_producer(filtered_data)
total_milk_produced = get_total_milk_produced(filtered_data)
overall_total_milk_produced = get_overall_total_milk_produced()

col1, col2, col3 = st.columns(3)
with col1:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Highest Milk Producer</h4>
                <p style='color: #e44b8d'>{highest_producer if highest_producer else 'N/A'} : {highest_production:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying highest producer: {e}")
with col2:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4 style="font-size: 23.6px;">Total Milk Produced (Start-End Date)</h4>
                <p style='color: #e69b00'>{total_milk_produced:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying total milk produced: {e}")
with col3:
    try:
        st.markdown(f"""
            <div style="border: 2px solid #e44b8d; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <h4>Overall Total Milk Produced</h4>
                <p style='color: #3b8132'>{overall_total_milk_produced:.2f} L</p>
            </div>
        """, unsafe_allow_html=True)
    except TypeError as e:
        st.error(f"Error in displaying overall total milk produced: {e}")

# Display the DataFrame below the dashboard tiles
update_table(filtered_data)
# Create interactive widgets
selected_index = st.selectbox(
    'Select Record to Edit/Delete',
    options=[None] + list(filtered_data.index),
    format_func=lambda x: 'No selection' if x is None else x
)
input_date = st.date_input('Input Date', value=date.today())
cow_name_input = st.text_input('Cow Name')
morning_input = st.number_input('Morning Production (L)', step=0.1)
noon_input = st.number_input('Noon Production (L)', step=0.1)
evening_input = st.number_input('Evening Production (L)', step=0.1)

# Arrange buttons in a row format
col1, col2, col3 = st.columns(3)
with col1:
    add_button = st.button('Add Record', key='add_button')
if st.session_state.user_role in ['Manager', 'Admin']:
    with col2:
        edit_button = st.button('Edit Record', key='edit_button')
    with col3:
        delete_button = st.button('Delete Record', key='delete_button')

# Function to add a new record to the DataFrame
def add_record():
    if not cow_name_input:
        st.error('Cow Name cannot be empty')
        return
    new_record = pd.DataFrame({
        'Date': [input_date],
        'Cow Name': [cow_name_input],
        'Morning': [morning_input],
        'Noon': [noon_input],
        'Evening': [evening_input],
        'Total': [morning_input + noon_input + evening_input]
    })
    st.session_state.milk_data = pd.concat([st.session_state.milk_data, new_record], ignore_index=True)
    st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
    st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
    st.success('Successfully Added!')
    st.rerun()  # Refresh the page

# Function to edit a selected record in the DataFrame
def edit_record():
    if not cow_name_input:
        st.error('Cow Name cannot be empty')
        return
    if selected_index is not None:
        st.session_state.milk_data.at[selected_index, 'Date'] = input_date
        st.session_state.milk_data.at[selected_index, 'Cow Name'] = cow_name_input
        st.session_state.milk_data.at[selected_index, 'Morning'] = morning_input
        st.session_state.milk_data.at[selected_index, 'Noon'] = noon_input
        st.session_state.milk_data.at[selected_index, 'Evening'] = evening_input
        st.session_state.milk_data.at[selected_index, 'Total'] = morning_input + noon_input + evening_input
        st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
        st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
        st.success('Successfully Edited!')
        st.rerun()  # Refresh the page

# Function to delete a selected record from the DataFrame
def delete_record():
    if selected_index is not None:
        st.session_state.milk_data = st.session_state.milk_data.drop(selected_index).reset_index(drop=True)
        st.session_state.milk_data['Date'] = pd.to_datetime(st.session_state.milk_data['Date'])  # Ensure Date column is datetime
        st.session_state.milk_data.to_csv('milk_production.csv', index=False)  # Save to CSV
        st.success('Successfully Deleted!')
        st.rerun()  # Refresh the page

# Handle button clicks
if add_button:
    add_record()

if st.session_state.user_role in ['Manager', 'Admin']:
    if edit_button:
        edit_record()
    if delete_button:
        delete_record()

# Create bar chart for total milk production over time
st.bar_chart(filtered_data.set_index('Date')['Total'])

# Create line chart for milk production over time for each cow
line_chart_data = filtered_data.pivot(index='Date', columns='Cow Name', values='Total')
st.line_chart(line_chart_data)
