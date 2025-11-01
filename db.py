import psycopg2
from psycopg2.extras import RealDictCursor

# Database connect
DB_CONNECT = {
    'host': 'localhost',
    'dbname': 'pet_grooming_logbook',
    'user': 'postgres',
    'password': '000925',
    'port': 5432
}

# Get database connection
def get_connection():
    return psycopg2.connect(**DB_CONNECT)
