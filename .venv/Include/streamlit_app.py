import streamlit as st
import os
from form.login import login, logout

# Initialize session state for user_role, logged_in, and page
if 'user_role' not in st.session_state:
    st.session_state.user_role = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = None

# --- PAGE SETUP ---
milk_page = st.Page(
    "views/milk.py",
    title="Milk Production Tracker",
    icon=":material/account_circle:",
    default=True,
)
sales_page = st.Page(
    "views/sales.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
)
inventory_page = st.Page(
    "views/inventory.py",
    title="Inventory",
    icon=":material/smart_toy:",
)
workers_page = st.Page(
    "views/workers.py",
    title="Workers",
    icon=":material/person:",
)
cattle_page = st.Page(
    "views/cattle.py",
    title="Cattle",
    icon=":material/agriculture:",
)
# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Milk": [milk_page],
        "Admin": [sales_page, inventory_page, workers_page, cattle_page],
    }
)

# --- SHARED ON ALL PAGES ---
current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, 'assets', 'logo.png')
image_path_2 = os.path.join(current_dir, 'assets', 'logo.png')
st.logo(image_path)  
#st.image(image_path_2, width=100)# Adjust the width as needed
st.sidebar.markdown("Made with Prescison")

# --- LOGIN/LOGOUT ---
if not st.session_state.logged_in:
    login()
else:
    st.sidebar.button('Logout', on_click=logout)
    # --- RUN NAVIGATION ---
    if st.session_state.page == 'Milk Production Tracker':
        pg.run()
