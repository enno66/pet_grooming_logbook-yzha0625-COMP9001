from db import get_connection
from psycopg2.extras import RealDictCursor
import psycopg2

def get_customer_pets(cid):
    """
    Get all pet information of this customer based on customer ID (cid)
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT * FROM pet WHERE owner_id = %s ORDER BY name"
        
        cur.execute(query, (cid,)) 
        
        pets = cur.fetchall() 
        
        return pets

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to query pets: {error}")
        return [] 
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
def get_pet_details(pid):
    """
    Get the detailed information of this pet based on the pet ID (pid)
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = "SELECT * FROM pet WHERE id = %s"
        
        cur.execute(query, (pid,)) 
        
        pet = cur.fetchone() # return a dictionary
        
        return pet

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to query pet details: {error}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
            
def create_appointment(cid, pid, sid, appointment_time, notes):
    """
    The customer creates a new appointment record
    """
    conn = None
    cur = None
    success = False
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        query = """
            INSERT INTO appointment (customer_id, pet_id, staff_id, appointment_time, customer_memo)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        cur.execute(query, (cid, pid, sid, appointment_time, notes))
        
        conn.commit()
        success = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to create appointment: {error}")
        if conn:
            conn.rollback()
            
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
    return success

def get_pet_appointments(pid):
    """
    Get all records of the pet (including employee name) based on pet ID (pid)
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
       
        # Using LEFT JOIN, even if 'staff_id' is NULL (not specified by the customer), you can still see this appointment record
        query = """
            SELECT 
                a.appointment_time, 
                a.status, 
                a.customer_memo, 
                a.staff_memo,
                a.staff_photo_path,
                s.sname AS staff_name 
            FROM 
                appointment a
            LEFT JOIN 
                staff s ON a.staff_id = s.sid
            WHERE 
                a.pet_id = %s
            ORDER BY 
                a.appointment_time DESC
        """
        
        cur.execute(query, (pid,)) 
        
        appointments = cur.fetchall()
        
        return appointments

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to query booking history: {error}")
        return []
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()