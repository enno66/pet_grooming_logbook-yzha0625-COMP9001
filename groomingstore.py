import streamlit as st
from modules.login_page import login_page
from modules.customer_home import customer_home_page
from modules.staff_home import staff_home_page
from modules.pet_history_page import pet_history_page
from modules.booking_page import booking_page


if __name__ == "__main__":
    # initialization session_state
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    
    if 'user_info' not in st.session_state:
        st.session_state['user_info'] = None
        
        
    # Only show the sidebar when the user already login
    if st.session_state['page'] != 'login':
        with st.sidebar:
            
            # Check if user_info exists
            if st.session_state['user_info']:
                st.write(f"Welcome, {st.session_state['user_info']['username']}")
            if st.button("Logout"):
                st.session_state['page'] = 'login'
                st.session_state['user_info'] = None
                st.rerun() # return to the login page

    # All of the pages link
    # Login page
    if st.session_state['page'] == 'login':
        user_info = login_page()
        if user_info:
            st.session_state['user_info'] = user_info
            if user_info['role'] == 'customer':
                st.session_state['page'] = 'customer_home'
                st.rerun()
            elif user_info['role'] == 'staff':
                st.session_state['page'] = 'staff_home'
                st.rerun()
                
    # Customer home page
    elif st.session_state['page'] == 'customer_home':
        customer_home_page(st.session_state['user_info'])
        
    # Pet oppintment history page
    elif st.session_state['page'] == 'pet_history':
        pet_history_page(
            st.session_state['user_info'], 
            st.session_state['current_pet_id'] )
    
    # Booking page 
    elif st.session_state['page'] == 'booking':
        booking_page(st.session_state['user_info'])
    
    # Staff home page
    elif st.session_state['page'] == 'staff_home':
        staff_home_page(st.session_state['user_info'])

    else:
        st.error("⚠️ Invalid page, return to login")
        st.session_state['page'] = 'login'