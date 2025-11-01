
# 🐾 FluffyTail Pet Grooming Logbook

Welcome to **FluffyTail**, an online pet grooming logbook system.
It’s not just a system, but a way to record every happy moment of our fluffy friends. 💕

---

## 🎨 Design Inspiration

❤️ The inspiration for **FluffyTail** comes from my love for pets — especially my own dogs, **Eggy** and **Diandian**.  
💙 As a pet owner, I realised that grooming appointments are often recorded in scattered ways (through phone calls, others via chat apps).  
💛 This can make it difficult for both customers and groomers to manage bookings, track grooming history, or view after photos.

**FluffyTail** aims to solve these problems by creating a simple online system:

- Allows customers to make grooming appointments easily.
- Let's staff manage bookings and upload pet photos after grooming.
- Provides a warm, personalised experience for both sides

---

## 🌟 Features

### Customer Module

1️⃣ Customer Login: 

- Select the customer role and login to the system after verifying user information.  

2️⃣ Pet information display: 

- The homepage displays all the pet information of the customer.  
- Automatically calculate age and Zodiac

3️⃣ Grooming appointment:  

- Customers can add appointment information.    
- Within the business hours limit (10:30–17:30), the appointment interval is 1 hour.    
- Customers can specify a groomer, but staff time slots that have been reserved cannot be booked again.  
- Customers can add a memo for pets when making an appointment.  


4️⃣ Display appointment history: 

- View all reservations for a pet, including reservation status and appointment time. 
- Completed appointments will display photos uploaded by employees.  

---

### Staff Module

1️⃣ Staff Login:

- Select the staff role and login after verifying information.  

2️⃣ Manage customer and pet information:   

- Fuzzy query of customer info.
- Create new customers.
- Add or edit pet information for existing customers.
- Edit pet personality.

3️⃣ Manage appointments:   

- View the staff’s own and all unassigned pending appointment information.
- Update appointment status.
- Take over appointments that are not allocated.
 
4️⃣ Upload grooming photos (File I/O)

- When the staff changes the reservation status to completed, they can upload photos of the pet after grooming, which the pet owner can view.  

---

## 🧠 Tech and Data Storage

- Core Language: Python  
- GUI Framework: Streamlit  
- Database: PostgreSQL  
- Python Libraries: streamlit, psycopg2, psycopg2.extras

---

## 🚀 How To Run

### Step 1: Install Required Libraries

This project relies on two Python libraries. Please run the following commands in your terminal:

--> pip install streamlit
--> pip install psycopg2-binary

### Step 2: Database Setup
Run the petgroominglogbook.sql file to create the database and all tables.

### Step 3: Run the Program
--> streamlit run Groomingstore.py
