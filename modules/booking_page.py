import streamlit as st
import datetime
from services.customer_services import get_customer_pets, create_appointment
from services.staff_services import get_all_staff, check_appointment

def get_time_slots():
    """
    Generate time options every hour between 10:30 - 16:30
    
    """
    slots = {}
    # (Hour, Min)
    times = [
        (10, 30), (11, 30), (12, 30), (13, 30),
        (14, 30), (15, 30), (16, 30) 
    ]
    
    for h, m in times:
        time_obj = datetime.time(h, m)
        time_str = time_obj.strftime("%I:%M %p") 
        slots[time_str] = time_obj
        
    return slots


def booking_page(user_info):
    
    st.title("🗓️ Make Appointment")
    st.info("💡 If you have any questions, please contact our store email: FluffyTails@gmail.com")
    st.markdown("---")
    
    # 1. Get the customer's ID
    cid = user_info['id']
    
    # 2. Get the customer's pet list
    pets = get_customer_pets(cid)
    if not pets:
        st.warning("You must add your pet before making an appointment!")
        return

    # 3. Get the staff list
    staff_list = get_all_staff()
    
    # --- Creat the dictionary ---
    
    # { 'Dandian': 1, 'Eggy': 2 }
    pet_options = {pet['name']: pet['id'] for pet in pets}
    
    # { 'Coco Lee': 1, 'David Kim': 2, ' ': None }
    staff_options = {staff['sname']: staff['sid'] for staff in staff_list}
    staff_options["Any Staff"] = None
    
    time_slots_options = get_time_slots()
    
    # --- Build an appointment form ---
    
    with st.form(key="appointment_form"):
        st.subheader("Please fill in the appointment details")
        
        # Choose the pet
        pet_name = st.selectbox("Choose your pet:", pet_options.keys())
        
        # Choose the date
        booking_date = st.date_input(
            "Choose the date:", 
            value=datetime.date.today() + datetime.timedelta(days=1)
        )
        
        # Choose the time
        time_slots = st.selectbox(
            "Choose the time (Opening hours 10:30-17:30):", 
            time_slots_options.keys()
        )
        
        # Choose the staff
        staff_name = st.selectbox(
            "Choose the staff:", 
            staff_options.keys()
        )
        
        # Add memo
        notes = st.text_area("Note (Please tell us your detailed requirements or tips!)")
        
        # Submit button
        submitted = st.form_submit_button("Confirm appointment")

        
        if submitted:
            # 1. Get the ID
            pid = pet_options[pet_name]
            sid = staff_options[staff_name]
            
            # 2. Combine the date and time
            booking_time = time_slots_options[time_slots]
            appointment_time = datetime.datetime.combine(booking_date, booking_time)
            
            # 3. Check the appointment conflict
            is_conflict = False
            # Check if the customer choose the staff
            if sid is not None:
                is_conflict = check_appointment(sid, appointment_time)
            
            if is_conflict:
                st.error(f"❌ Appointment failed!\n {staff_name} already has an appointment on {booking_date} at {time_slots}.")
            
            else:
                # If no conflict
                success = create_appointment(cid, pid, sid, appointment_time, notes)
                
                if success:
                    st.success(f"🎉 Appointment successful! \n {staff_name} will be waiting for {pet_name} on {booking_date} at {time_slots}.")
                    st.balloons()
                else:
                    st.error("❌ Appointment failed, please check the time or contact us. ")

    st.markdown("---")
    # Return button
    if st.button("⬅️ Return to homepage"):
        st.session_state['page'] = 'customer_home'
        st.rerun()