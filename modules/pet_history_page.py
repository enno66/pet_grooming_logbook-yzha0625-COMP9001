import streamlit as st
from services.customer_services import get_pet_details, get_pet_appointments

def pet_history_page(user_info, pet_id):
    
    # Get the information of the pet
    pet = get_pet_details(pet_id)
    
    if pet is None:
        st.error("Unable to load pet information, please try again.")
        return

    # Title
    st.title(f"🐾 {pet['name']}'s Booking history")
    st.markdown("---")

    st.subheader("Appointment and grooming history")
    bookings = get_pet_appointments(pet_id)

    if not bookings:
        st.info("This pet does not have any appointment yet. ")
    
    else:
        # Draw a sheet
        # Set width of columns
        cols = st.columns([1.5, 1.5, 1.5, 2, 2]) 
        
        cols[0].markdown("⏰Time")
        cols[1].markdown("💡Status")
        cols[2].markdown("💇Groomer")
        cols[3].markdown("📒My Memo")
        cols[4].markdown("📒Staff Memo")
        st.divider()

        # Loop through all of the booking info
        for row in bookings:
            cols = st.columns([1.5, 1.5, 1.5, 2, 2])
            
            # Column 1: Time
            cols[0].write(row['appointment_time'].strftime("%Y-%m-%d %H:%M"))
            
            # Column 2: Status
            if row['status'] == 'pending':
                cols[1].warning(row['status'])
            elif row['status'] == 'confirmed':
                cols[1].info(row['status'])
            elif row['status'] == 'completed':
                cols[1].success(row['status'])
            else:
                cols[1].write(row['status'])
            
            # Column 3: Groomer
            cols[2].write(row['staff_name'] if row['staff_name'] else "any groomer")
            
            # Column 4: My Memo 
            cols[3].write(row['customer_memo'] if row['customer_memo'] else " ")
            
            # Column 5: Staff Memo
            cols[4].write(row['staff_memo'] if row['staff_memo'] else " ")
            
            if row['staff_photo_path']:
                try:
                    cols[4].image(row['staff_photo_path'], width=100, caption="Photos after grooming")
                except:
                    cols[4].error("Photos lost")
            
            st.divider() # Draw a dividing line between each record

    # Return button
    if st.button("⬅️ Return to my pet list"):
        st.session_state['page'] = 'customer_home'
        if 'current_pet_id' in st.session_state:
            del st.session_state['current_pet_id'] 
        st.rerun()