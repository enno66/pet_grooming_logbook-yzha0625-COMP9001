from db import get_connection
from psycopg2.extras import RealDictCursor
import psycopg2

def get_all_staff():
    """
    Get all employee IDs and names
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
    
        query = "SELECT sid, sname FROM staff"
        
        cur.execute(query)
        staff_list = cur.fetchall() # [ {'sid': 1, 'sname': 'Coco Lee'}, ... ]
        
        return staff_list

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to query employee list: {error}")
        return []
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            

def check_appointment(sid, appointment_time):
    """
    Check whether an employee (sid) has an appointment at a certain time (appointment_time)
    Return True or False
    """
    conn = None
    cur = None
    is_conflict = False # Set the default
    
    try:
        conn = get_connection()
        cur = conn.cursor() 
        
        # Query the number of records in the 'appointment' table that match the employee ID and timestamp exactly.
        query = "SELECT COUNT(*) FROM appointment WHERE staff_id = %s AND appointment_time = %s"
        
        cur.execute(query, (sid, appointment_time))
        
        count = cur.fetchone()[0] # Get the number in (0,) or (1,)
        
        if count > 0:
            is_conflict = True # Record found, is conflict

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to query conflict: {error}")
        # If the check fails, we also assume a conflict to be safe
        is_conflict = True 
            
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
    return is_conflict


def get_my_appointments(sid):
    """
    Get only 'Pending' or 'Confirmed' appointments assigned to a specific staff (sid)
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                a.id AS appointment_id, a.appointment_time, a.status,
                a.customer_memo, p.name AS pet_name, c.cname AS customer_name
            FROM appointment a
            JOIN pet p ON a.pet_id = p.id
            JOIN customer c ON a.customer_id = c.cid
            WHERE
                a.staff_id = %s 
                AND (a.status = 'pending' OR a.status = 'confirmed')
            ORDER BY a.appointment_time ASC
        """
        cur.execute(query, (sid,))
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to check staff appointment: {error}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_unassigned_appointments():
    """
    Get all appointments with staff_id IS NULL and status 'pending'
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                a.id AS appointment_id, a.appointment_time, a.status,
                a.customer_memo, p.name AS pet_name, c.cname AS customer_name
            FROM appointment a
            JOIN pet p ON a.pet_id = p.id
            JOIN customer c ON a.customer_id = c.cid
            WHERE
                a.staff_id IS NULL
                AND a.status = 'pending'
            ORDER BY a.appointment_time ASC
        """
        cur.execute(query) 
        return cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to check unassigned appointments: {error}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
        
        
def update_appointment(appointment_id, new_status=None, staff_memo=None, new_staff_id=None, staff_photo_path=None):
    """
    - new_status: 'confirmed', 'completed'
    - staff_memo
    - new_staff_id: When staff take over the appintment, they fill in their own IDs.
    """
    conn = None
    cur = None
    success = False
    
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        #Query when satisfied the condition
        query_parts = []
        params = []
        
        if new_status is not None:
            query_parts.append("status = %s")
            params.append(new_status)
            
        if staff_memo is not None:
            query_parts.append("staff_memo = %s")
            params.append(staff_memo)
            
        if new_staff_id is not None:
            query_parts.append("staff_id = %s")
            params.append(new_staff_id)
            
        if staff_photo_path is not None:
            query_parts.append("staff_photo_path = %s")
            params.append(staff_photo_path)
        
        # If nothing pass, there's no need to update
        if not query_parts:
            return False
        params.append(appointment_id)
 
        query = f"UPDATE appointment SET {', '.join(query_parts)} WHERE id = %s"
        
        cur.execute(query, tuple(params))
        
        conn.commit()
        
        if cur.rowcount > 0:
            success = True

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to update appointment: {error}")
        if conn:
            conn.rollback()
            
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
            
    return success

def search_customers(search_term):
    """
    Search the customer
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT cid, cname, email, contact_info
            FROM customer
            WHERE cname ILIKE ('%%' || %s || '%%')
            ORDER BY cname
        """
        cur.execute(query, (search_term,))
        
        return cur.fetchall()
    
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to search for customers: {error}")
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_customer_account(cname, email, contact, username, password):
    """
    Create a transaction for a new customer and their login account
    """
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        customer_query = """
            INSERT INTO customer (cname, email, contact_info)
            VALUES (%s, %s, %s)
            RETURNING cid
        """
        cur.execute(customer_query, (cname, email, contact))
        new_cid = cur.fetchone()[0]
        
        if new_cid:
            account_query = """
                INSERT INTO account (username, password, role, user_id)
                VALUES (%s, %s, 'customer', %s)
            """
            cur.execute(account_query, (username, password, new_cid))
            conn.commit()
            return True, f"Customer created successfully {cname} (ID: {new_cid})！"
        else:
            raise Exception("Failed to get new customer's cid")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to create new customer: {error}")
        if conn:
            conn.rollback()
        return False, str(error) 
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def create_pet(owner_id, name, birthday, gender, personality):
    """
    Create a new pet for the specified customer
    """
    conn = None
    cur = None
    success = False
    try:
        conn = get_connection()
        cur = conn.cursor()
        # ✅ Match to the pet (owner_id, name, birthday, gender, personality)
        query = """
            INSERT INTO pet (owner_id, name, birthday, gender, personality)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (owner_id, name, birthday, gender, personality))
        conn.commit()
        success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to create pet: {error}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return success

def update_pet_personality(pid, new_personality):
    """
    Update pet's personality notes
    """
    conn = None
    cur = None
    success = False
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = "UPDATE pet SET personality = %s WHERE id = %s"
        cur.execute(query, (new_personality, pid))
        conn.commit()
        if cur.rowcount > 0:
            success = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Failed to update pet personality: {error}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    return success