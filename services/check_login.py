from db import get_connection
from psycopg2.extras import RealDictCursor
import psycopg2

def check_login(username, password, role):
    """
    Verify the login identity 
    Return the corresponding cid or sid, or None if failed.
    """
    conn = None
    cur = None
    
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
            SELECT user_id FROM account
            WHERE username = %s AND password = %s AND role = %s
        """
        
        cur.execute(query, (username, password, role.lower()))
        
        result = cur.fetchone()
        
        if result:
            # If the login is successful, get this ID
            return result['user_id']
        else:
            # Login failed (username, password or role mismatch)
            return None

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")
        return None
        
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
