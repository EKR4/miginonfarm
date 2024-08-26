import streamlit as st

def login():
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    role = st.selectbox('Role', ['Worker', 'Manager', 'Admin'])
    login_button = st.button('Login')

    if login_button:
        # Here you can add your authentication logic
        if username and password:
            st.session_state.user_role = role
            st.session_state.logged_in = True
            st.session_state.page = 'Milk Production Tracker'
            st.success(f'Logged in as {role}')
            st.rerun()  # Force a rerun of the script
        else:
            st.error('Please enter a valid username and password')

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.page = None
    st.success('Logged out successfully')
