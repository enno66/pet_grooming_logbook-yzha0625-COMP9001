import streamlit as st
from services.staff_services import get_my_appointments, get_unassigned_appointments, update_appointment, search_customers, create_customer_account, create_pet, update_pet_personality
from services.customer_services import get_customer_pets
from modules.utils import save_uploaded_file

def staff_home_page(user_info):
    
    st.title(f"🛠️ Staff Home")
    
    st.markdown(f"🧑‍⚕️ Hi, {user_info['username']}! Welcome, {user_info['username']}!")
    
    st.markdown("---")
    
    st.subheader("📋 Features")

    option = st.selectbox(
        "Please select a function:",
        (
            "Manage Appointments", 
            "Manage Customer & Pet Records", 
        )
    )

    if option == "Manage Appointments":
        tab1, tab2 = st.tabs([
            "⭐ My Appointments", 
            "🙋 Unassigned"
        ])

        # --- 1. My appointments ---
        with tab1:
            st.subheader("Appointments assigned to you")

            my_appointments = get_my_appointments(user_info['id']) 

            if not my_appointments:
                st.success("🎉 Congratulations! You have no pending appointments. ")
            else:
                st.info(f"You have {len(my_appointments)} pending appointments: ")

                for appt in my_appointments:
                    time_str = appt['appointment_time'].strftime("%Y-%m-%d %H:%M")
                    with st.expander(f"**{time_str}** - {appt['pet_name']} (Owner: {appt['customer_name']}) - Status: {appt['status']}"):
                        
                        with st.form(key=f"form_my_appt_{appt['appointment_id']}"):

                            st.write(f"Pet: {appt['pet_name']}")
                            st.write(f"Owner: {appt['customer_name']}")
                            st.write(f"Customer Memo: {appt['customer_memo'] if appt['customer_memo'] else ' '}")

                            st.markdown("---")
                            uploaded_photo = st.file_uploader(
                                        "Upload Grooming Photo", 
                                        type=["jpg", "png", "jpeg"],
                                        key=f"photo_{appt['appointment_id']}"
                            )
                            staff_memo_input = st.text_area("Staff Memo:", key=f"memo_{appt['appointment_id']}")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                confirm_pressed = st.form_submit_button("✅ Confirm")
                            with col2:
                                complete_pressed = st.form_submit_button("🏁 Complete")
                                
                            #Button logic
                            if confirm_pressed:
                                # If "Confirm" --- don't need to leave memo
                                success = update_appointment(
                                    appt['appointment_id'], 
                                    new_status='confirmed'
                                )
                                if success:
                                    st.success("Appointment Confirmed!")
                                    st.rerun() 
                                else:
                                    st.error("Operation failed")
                            
                            if complete_pressed:
                                # If "Complete" -- update the memo with button
                                # ✅ upload photo
                                new_photo_path = None
                                if uploaded_photo is not None:
                                    # Call save_uploaded_file function to save the photo
                                    new_photo_path = save_uploaded_file(uploaded_photo, appt['appointment_id'])

                                    if new_photo_path is None:
                                        st.error("Photo save failed! But the appointment will still try to update. ")
                                
                                # Update status
                                success = update_appointment(
                                    appt['appointment_id'], 
                                    new_status='completed',
                                    staff_memo=staff_memo_input,
                                    staff_photo_path=new_photo_path
                                )

                                if success: 
                                    st.success("Appointment marked as complete! ")
                                    st.rerun() 
                                else: 
                                    st.error("Operation Failed")
                        
        # -- 2. Unassigned appointments ---
        with tab2:
            st.subheader("Appointments waiting for staff...")

            unassigned_appointments = get_unassigned_appointments()

            if not unassigned_appointments:
                st.info("You have no pending appointments. ")
            else:
                for appt in unassigned_appointments:
                    time_str = appt['appointment_time'].strftime("%Y-%m-%d %H:%M")
                    with st.expander(f"**{time_str}** - {appt['pet_name']} (Owner: {appt['customer_name']})"):
                        st.write(f"Pet: {appt['pet_name']}")
                        st.write(f"Owner: {appt['customer_name']}")
                        st.write(f"Customer Memo: {appt['customer_memo'] if appt['customer_memo'] else ' '}")

                        if st.button("🙋‍♂️ Assign to Me", key=f"assign_{appt['appointment_id']}"):
                            success = update_appointment(
                                appt['appointment_id'], 
                                new_staff_id=user_info['id'] # ✅ Update the staff id
                            )
                            if success:
                                st.success(f"You have assigned this appointment to yourself!")
                                st.rerun() # Refresh to tab 1
                            else:
                                st.error("Operation failed")
                        st.divider()
        
    elif option == "Manage Customer & Pet Records":
        st.subheader("Manage Customer & Pet Records")

        # --- 1. Search Customer ---
        st.markdown("---")
        st.markdown("🔍 Search Customer Here")
        search_term = st.text_input("[Search by customer name:]")
        
        if search_term:
            customers = search_customers(search_term)
            if customers:
                st.success(f"Found {len(customers)} customer(s):")
                
                # --- 2. Show "Add/Edit" option for each customer ---
                for customer in customers:
                    with st.expander(f"👤 **{customer['cname']}** (Email: {customer['email']})"):
                        
                        tab_edit, tab_add = st.tabs(["✏️ Edit existing pet", "➕ Add new pet"])
                        
                        # ---  Edit existing pet ---
                        with tab_edit:
                            st.markdown(f"**Editing pet information for {customer['cname']}**")
                            pets = get_customer_pets(customer['cid']) 
                            if not pets:
                                st.info(f"{customer['cname']} haven't been registered any pet yet.")
                            else:
                                for pet in pets:
                                    with st.form(key=f"edit_pet_{pet['id']}"):
                                        st.write(f"🐾 **{pet['name']}** (ID: {pet['id']})")
                                        new_personality = st.text_area(
                                            "Personality:",
                                            value=pet['personality'] if pet['personality'] else ""
                                        )
                                        submitted_edit = st.form_submit_button("Save edit")
                                        if submitted_edit:
                                            success = update_pet_personality(pet['id'], new_personality)
                                            if success: st.success("Update successful! "); st.rerun()
                                            else: st.error("Update failed. ")
                                            
                        # --- Add a new pet ---
                        with tab_add:
                            st.markdown(f"**Adding a new pet for {customer['cname']}**")
                            with st.form(key=f"add_pet_for_{customer['cid']}"):
                                pet_name = st.text_input("Pet Name")
                                pet_gender = st.selectbox("Gender", ["Male", "Female", "Unknown"])
                                pet_birthday = st.date_input("Birthday")
                                pet_personality = st.text_area("Personality")
                                
                                submitted_add = st.form_submit_button("Add Pet")
                                if submitted_add:
                                    success = create_pet(
                                        customer['cid'], pet_name, pet_birthday, pet_gender, pet_personality
                                    )
                                    if success:
                                        st.success(f"Successfully added {pet_name} for {customer['cname']}! ")
                                        st.rerun()
                                    else:
                                        st.error("Add failed. ")
            
            else:
                st.warning(f"No customer named '{search_term}' found.")
                
        # --- 3. Create new customer (When customer not found) ---
        st.markdown("---")
        st.markdown("#### Create New Customer")
        with st.expander("If you can't find the customer, create a new account here ➕"):
            with st.form(key="create_customer_form"):
                st.markdown("Customer Info")
                cname = st.text_input("Full Name")
                email = st.text_input("Email")
                contact = st.text_input("Contact Info")
                st.markdown("Login Account")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted_create = st.form_submit_button("Create")
                
                if submitted_create:
                    success, message = create_customer_account(
                        cname, email, contact, username, password
                    )
                    if success:
                        st.success(message)
                    else:
                        st.error(f"Create Failed : {message}")
        