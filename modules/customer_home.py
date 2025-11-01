import streamlit as st
from services.customer_services import get_customer_pets
from modules.utils import calculate_age, get_zodiac

def customer_home_page(user_info):
    st.title("🐾 Customer Home")

    st.markdown(f"👤 Welcome, {user_info['username']}! ")
    st.markdown("---")
    st.subheader("📋 Features")
    
    option = st.selectbox(
        "Please select a function:",
        ("View My Pets", "Make Appointment")
    )

    if option == "View My Pets":
        # Call function to get all of the pets of this customer
        my_pets = get_customer_pets(user_info['id']) 
        
        if not my_pets:
            st.info("You haven't added any pets yet.")
            
        else:
            st.subheader(f"You have registered {len(my_pets)} pets in total:")
            
            # 2. Loop through the pet list
            for pet in my_pets:
                
                with st.expander(f"🐾 **{pet['name']}** ({pet['personality']})"):
                    st.write(f"**Gender:** {pet['gender']}")
                    
                    # Calculate the age and zodiac
                    age = calculate_age(pet['birthday'])
                    zodiac = get_zodiac(pet['birthday'])

                    # Show the info
                    st.write(f"**Birthday:** {pet['birthday']} (Age: {age} | Zodiac: {zodiac})")
                    
                    st.write(f"**Personality:** {pet.get('personality', ' ')}")
                    
                    if st.button("View appointment history", key=f"history_{pet['id']}"):
                        st.session_state['page'] = 'pet_history'
                        st.session_state['current_pet_id'] = pet['id']
                        st.rerun()
                        
    elif option == "Make Appointment":
        st.session_state['page'] = 'booking'
        st.rerun()