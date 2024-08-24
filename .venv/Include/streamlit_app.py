import streamlit as st
import os

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


# --- RUN NAVIGATION ---
pg.run()